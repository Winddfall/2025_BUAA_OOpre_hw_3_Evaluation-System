import random
import os
import math # 保持math导入的习惯

from id_pools import (
    adventurer_id_pool, bottle_id_pool, sword_id_pool,
    magicbook_id_pool, armour_id_pool, spell_id_pool
)

# --- 新增配置项 ---
# 有多大概率会尝试生成让“死亡冒险者”执行操作的指令
PROB_USE_DEAD_ACTOR = 0.2

def generate_test_case(test_case_id, num_operations):
    """
    根据新的需求生成一个测试用例，并将其写入文件。
    此版本会特意生成让死亡冒险者执行操作的样例。
    :param test_case_id: 测试用例的ID，用于命名文件。
    :param num_operations: 要生成的指令数量。
    """
    
    bottle_types = ["HpBottle", "AtkBottle", "DefBottle", "ManaBottle"]
    spell_types = ["HealSpell", "AttackSpell"]

    # --- 物品类型定义 ---
    ITEM_TYPE_BOTTLE = "Bottle"
    ITEM_TYPE_SWORD = "Sword"
    ITEM_TYPE_MAGICBOOK = "Magicbook"
    ITEM_TYPE_ARMOUR = "Armour"

    # --- 背包容量限制 --
    BOTTLE_CAPACITY = 10
    WEAPON_LIMIT = 1  # 只能携带一件Sword或一件Magicbook
    ARMOUR_LIMIT = 1  # 只能携带一件Armour

    # --- 状态追踪变量 ---
    existing_adv = set() # 存放已经存在的冒险者ID
    # 'money'属性已包含在内
    adv_attributes = {}  # {adv_id: {'hp': int, 'atk': int, 'def': int, 'mana': int, 'money': int}} 冒险者状态
    adv_owned_items = {}  # {adv_id: {item_id: item_type_str}} 拥有的物品（不包括法术）
    adv_backpacks = {}  # {adv_id: {'bottles': list, 'sword': str, 'magicbook': str, 'armour': str}} 背包内的物品，按类型分类
    adv_learned_spells = {}  # {adv_id: {spell_id: {'type': str, 'mana_cost': int, 'power': int}}} 学习的法术
    item_details = {}  
    '''
    {
        item_id: {'type': str, 'effect': int}, 药水瓶
        item_id: {'type': str, 'ce': int}, 装备
        item_id: {'type': str, 'mana_cost': int, 'power': int} 法术
    }
    '''
    
    # 用来记录已使用的所有ID，确保全局唯一性
    used_ids = set()

    def get_item_category(item_id):
        """根据物品ID判断物品类别"""
        if item_id in sword_id_pool:
            return ITEM_TYPE_SWORD
        elif item_id in magicbook_id_pool:
            return ITEM_TYPE_MAGICBOOK
        elif item_id in armour_id_pool:
            return ITEM_TYPE_ARMOUR
        elif item_id in bottle_id_pool:
            return ITEM_TYPE_BOTTLE
        else:
            return None

    def discard_oldest_bottle(adv_id: str) -> str:
        """顶替最早的药水瓶，并返回被顶替药水瓶的ID"""
        if adv_id not in adv_backpacks:
            return None
        bottles = adv_backpacks[adv_id].get('bottles', [])
        if not bottles:
            return None
        
        # 获取最早的药水瓶（列表第一个）并移除
        oldest_bottle_id = bottles.pop(0) 
        return oldest_bottle_id

    def remove_weapon_if_exists(adv_id):
        """如果有武器装备，移除现有的武器（为新武器让位），返回被替换的ID"""
        if adv_id not in adv_backpacks:
            return None

        backpack = adv_backpacks[adv_id]
        
        old_weapon_id = None
        if backpack.get('sword') is not None: # 如果是剑
            old_weapon_id = backpack.pop('sword')
        elif backpack.get('magicbook') is not None: # 如果是魔法书
            old_weapon_id = backpack.pop('magicbook')
            
        return old_weapon_id

    def remove_armour_if_exists(adv_id):
        """如果有装甲装备，移除现有的装甲（为新装甲让位），返回被替换的ID"""
        if adv_id not in adv_backpacks:
            return None

        backpack = adv_backpacks[adv_id]
        if backpack.get('armour') is not None:
            old_armour_id = backpack.pop('armour')
            return old_armour_id
        return None

    def calculate_kill_gold(killed_adv_id, killer_adv_id):
        """
        计算击杀获得的金币数
        金币计算公式：被击杀者金币 + 药水瓶effect总和 + 装备CE总和 (注意：是拥有的物品，不是携带的)
        """
        # 被击杀者拥有的金币
        killed_money = adv_attributes[killed_adv_id].get('money', 0)

        # 计算药水瓶effect总和
        bottle_effect_sum = 0
        equipment_ce_sum = 0
        owned_items = adv_owned_items.get(killed_adv_id, {})
        
        for item_id, item_type_str in owned_items.items():
            if item_id in item_details:
                item_info = item_details[item_id]
                
                # 药水瓶 effect 总和
                if item_type_str in bottle_types and 'effect' in item_info:
                    bottle_effect_sum += item_info['effect']
                
                # 装备 CE 总和
                elif item_type_str in [ITEM_TYPE_SWORD, ITEM_TYPE_MAGICBOOK, ITEM_TYPE_ARMOUR] and 'ce' in item_info:
                    equipment_ce_sum += item_info['ce']

        total_gold = killed_money + bottle_effect_sum + equipment_ce_sum
        return total_gold

    def calculate_defense_power(adv_id):
        """计算冒险者的最终防御力（基础防御 + 携带装甲CE）"""
        # 基础防御力
        base_def = adv_attributes[adv_id].get('def', 0)

        # 携带装甲的CE加成
        backpack = adv_backpacks.get(adv_id, {})
        armor_id = backpack.get('armour')

        armor_defense_ce = 0
        if armor_id and armor_id in item_details:
            armor_defense_ce = item_details[armor_id]['ce']

        return base_def + armor_defense_ce

    def calculate_attack_power(adv_id):
        """计算冒险者的最终攻击力（基础攻击 + 携带Sword CE）"""
        # 基础攻击力
        base_atk = adv_attributes[adv_id].get('atk', 0)

        # 携带Sword的CE加成
        backpack = adv_backpacks.get(adv_id, {})
        sword_id = backpack.get('sword')

        weapon_attack_ce = 0
        if sword_id and sword_id in item_details:
            weapon_attack_ce = item_details[sword_id]['ce']

        return base_atk + weapon_attack_ce

    def get_magicbook_ce_value(adv_id):
        """获取冒险者携带的魔法书的CE值（用于魔法攻击判定和消耗）"""
        backpack = adv_backpacks.get(adv_id, {})
        magicbook_id = backpack.get('magicbook')

        if magicbook_id and magicbook_id in item_details:
            return item_details[magicbook_id]['ce']

        return 0

    def perform_battle(attacker_id, target_ids):
        """执行战斗逻辑 (target_ids 必须是活着的冒险者)"""
        
        # 1. 计算攻击者的最终攻击力、魔力、魔法书CE
        attacker_final_atk = calculate_attack_power(attacker_id)
        attacker_mana = adv_attributes[attacker_id].get('mana', 0)
        magicbook_ce = get_magicbook_ce_value(attacker_id)
        
        # 2. 确定受攻击方的整体防御能力 (Max Def)
        target_defs = [calculate_defense_power(tid) for tid in target_ids]
        if not target_defs:
            return False, ["没有可攻击的存活目标"]
            
        overall_def = max(target_defs)
        
        # 3. 判断攻击类型和成功条件
        backpack = adv_backpacks.get(attacker_id, {})
        carried_sword = backpack.get('sword')
        carried_magicbook = backpack.get('magicbook')
        
        is_magic_attack = carried_magicbook is not None # Magicbook is present
        
        battle_successful = False
        damage = 0
        
        if is_magic_attack:
            # 魔法攻击：Attacker Mana >= Magicbook CE
            if attacker_mana >= magicbook_ce and magicbook_ce > 0:
                battle_successful = True
                # 魔法攻击伤害：所有被攻击者的体力值减去攻击者的攻击力
                damage = attacker_final_atk
                # 消耗魔力
                adv_attributes[attacker_id]['mana'] -= magicbook_ce
            
        else: # Physical attack: carried_sword is not None or no weapon
            # 物理攻击：Attacker Final ATK > Overall Defense
            if attacker_final_atk > overall_def:
                battle_successful = True
                # 物理攻击伤害：攻击者的攻击力 - 整体防御能力
                damage = attacker_final_atk - overall_def

        battle_results = []
        
        if battle_successful and damage > 0:
            for target_id in target_ids:
                adv_attributes[target_id]['hp'] -= damage
                
                # 检查是否击杀
                if adv_attributes[target_id]['hp'] <= 0:
                    adv_attributes[target_id]['hp'] = 0
                    # 击杀成功，计算并转移金币
                    kill_gold = calculate_kill_gold(target_id, attacker_id)
                    if kill_gold > 0:
                        adv_attributes[attacker_id]['money'] += kill_gold 
                    
                
            return True, battle_results # 战斗结果不在这里打印，由外部主程序处理
            
        return False, ["战斗失败或伤害为0"]

    def get_unused_id(pool):
        """从ID池中获取一个未使用的ID"""
        available_ids = [_id for _id in pool if _id not in used_ids]
        if not available_ids: return None
        new_id = random.choice(available_ids)
        used_ids.add(new_id)
        return new_id

    if not os.path.exists("input_data"):
        os.makedirs("input_data")

    with open(f"input_data/input_{test_case_id}.txt", "w") as f_input:
        # 第一行写入操作总数
        f_input.write(str(num_operations) + "\n")
        
        # 修复：将计数器变量 '_' 替换为 'op_count' 以避免命名冲突和TypeError
        op_count = 0 
        while op_count < num_operations:
            line = ""
            living_adv = [adv for adv in existing_adv if adv_attributes[adv]['hp'] > 0] # 更新存活冒险者们
            dead_adv = [adv for adv in existing_adv if adv_attributes[adv]['hp'] <= 0] # 更新死亡冒险者们
            
            # --- 动态确定可执行的操作 ---
            possible_ops = []
            # 存在还没使用的冒险者id
            if any(adv not in used_ids for adv in adventurer_id_pool): possible_ops.append("aa")

            if existing_adv: # 只要有冒险者存在，就可以考虑这些操作，即使操作者是死的
                # 检查是否存在未使用的药水瓶ID
                if any(bot not in used_ids for bot in bottle_id_pool): possible_ops.append("ab")
                # 检查三个装备池中是否有可用ID
                equipment_pools = [sword_id_pool, magicbook_id_pool, armour_id_pool]
                if any(any(equ not in used_ids for equ in pool) for pool in equipment_pools):
                    possible_ops.append("ae")
                # 检查是否存在未使用的法术ID
                if any(spe not in used_ids for spe in spell_id_pool): possible_ops.append("ls")
                # 检查是否存在冒险者持有物品不为空
                if any(adv_owned_items.get(adv) for adv in existing_adv): possible_ops.append("ri")
                # 检查是否存在冒险者持有物品不为空且该冒险者有未放进背包的物品
                def has_uncarried_items(adv_id):
                    owned_items = set(adv_owned_items.get(adv_id, {}).keys())
                    backpack = adv_backpacks.get(adv_id, {'bottles': [], 'sword': None, 'magicbook': None, 'armour': None})
                    carried_items = set()
                    # 添加药水瓶
                    carried_items.update(backpack.get('bottles', []))
                    # 添加剑
                    if backpack.get('sword') is not None:
                        carried_items.add(backpack['sword'])
                    # 添加魔法书
                    if backpack.get('magicbook') is not None:
                        carried_items.add(backpack['magicbook'])
                    # 添加装甲
                    if backpack.get('armour') is not None:
                        carried_items.add(backpack['armour'])
                    return bool(owned_items - carried_items)

                if any(adv_owned_items.get(adv) and has_uncarried_items(adv) for adv in existing_adv):
                    possible_ops.append("ti")
                # 检查是否有冒险者可以执行 use 操作
                for adv in existing_adv:
                    # 检查是否携带药水或学会了法术
                    carried_bottles = adv_backpacks.get(adv, {}).get('bottles', [])
                    has_learned_spell = bool(adv_learned_spells.get(adv))
                    if carried_bottles or has_learned_spell:
                        possible_ops.append("use")
                        break
                # 检查是否有冒险者可以执行购买操作（有可用物品ID）
                for adv in existing_adv:
                    # 检查是否有可购买的物品
                    has_available_bottles = any(bot not in used_ids for bot in bottle_id_pool)
                    has_available_equipment = any(any(equ not in used_ids for equ in pool) for pool in equipment_pools)
                    if has_available_bottles or has_available_equipment:
                        possible_ops.append("bi")
                        break
                # 检查是否有冒险者可以执行战斗操作（有其他存活冒险者）
                if len(living_adv) >= 1: # 战斗者可以是死的，但目标必须是活的
                    # 目标必须存在且全部存活，且不能包含攻击者自己 (这个复杂条件留给fight指令内部检查)
                    if len(existing_adv) >= 2:
                        possible_ops.append("fight")
            
            if not possible_ops:
                print(f"Warning: No more possible operations for test case {test_case_id}. Stopping early.")
                break

            # --- 根据权重选择一种指令 ---
            weights_map = {"aa": 0.10, "ab": 0.10, "ae": 0.10, "ls": 0.10, "ti": 0.10, "use": 0.10, "ri": 0.08, "bi": 0.15, "fight": 0.17}
            op_weights = [weights_map.get(op, 0) for op in possible_ops]
            op_type = random.choices(possible_ops, weights=op_weights, k=1)[0]

            # --- 生成具体指令并更新状态 ---
            actor_id, actor_is_alive = None, False

            if op_type == "aa":
                # ... aa logic (same as before)
                new_adv_id = get_unused_id(adventurer_id_pool)
                if new_adv_id:
                    line = f"aa {new_adv_id}\n"
                    existing_adv.add(new_adv_id)
                    adv_attributes[new_adv_id] = {'hp': 500, 'atk': 1, 'def': 0, 'mana': 10, 'money': 50} # 冒险者属性
                    adv_owned_items[new_adv_id] = {} # 冒险者拥有的物品
                    adv_backpacks[new_adv_id] = {
                        'bottles': [],  # 药水瓶列表，保持添加顺序
                        'sword': None,  # Sword装备ID
                        'magicbook': None,  # Magicbook装备ID
                        'armour': None  # Armour装备ID
                    } # 冒险者背包，按类型分类
                    adv_learned_spells[new_adv_id] = {} # 冒险者学会的法术
            
            elif op_type in ["ab", "ae", "ls"]:
                # ... ab/ae/ls actor selection and logic (same as before)
                # 概率触发对死亡冒险者进行操作
                if dead_adv and random.random() < PROB_USE_DEAD_ACTOR: 
                    actor_id = random.choice(dead_adv)
                elif existing_adv: 
                    actor_id = random.choice(list(existing_adv))
                else: continue
                
                actor_is_alive = adv_attributes[actor_id]['hp'] > 0
                new_item_id = None
                
                if op_type == "ab":
                    new_item_id = get_unused_id(bottle_id_pool)
                    if new_item_id:
                        bot_type = random.choice(bottle_types)
                        effect = random.randint(1, 100)
                        line = f"ab {actor_id} {new_item_id} {bot_type} {effect}\n"
                        if actor_is_alive:
                            adv_owned_items[actor_id][new_item_id] = bot_type
                            item_details[new_item_id] = {'type': bot_type, 'effect': effect}
                elif op_type == "ae":
                    equipment_pools = [sword_id_pool, magicbook_id_pool, armour_id_pool]
                    available_pools = [pool for pool in equipment_pools if any(equ not in used_ids for equ in pool)]

                    if available_pools:
                        selected_pool = random.choice(available_pools)
                        new_item_id = get_unused_id(selected_pool)
                        ce = random.randint(1, 100)
                        if new_item_id:
                            
                            item_type_str = ""
                            if selected_pool == sword_id_pool:
                                item_type_str = "Sword"
                            elif selected_pool == magicbook_id_pool:
                                item_type_str = "Magicbook"
                            elif selected_pool == armour_id_pool:
                                item_type_str = "Armour"

                            line = f"ae {actor_id} {new_item_id} {item_type_str} {ce}\n"

                            if actor_is_alive:
                                adv_owned_items[actor_id][new_item_id] = item_type_str
                                item_details[new_item_id] = {'type': item_type_str, 'ce': ce}
                elif op_type == "ls":
                    new_item_id = get_unused_id(spell_id_pool)
                    if new_item_id:
                        spell_weights = [0.3, 0.7] # 治疗 攻击
                        spe_type = random.choices(spell_types, weights=spell_weights, k=1)[0]
                        # 确保 mana_cost 不为负
                        mana_cost = random.randint(0, adv_attributes[actor_id].get('mana', 10) + 5) 
                        power = random.randint(0, 500)
                        line = f"ls {actor_id} {new_item_id} {spe_type} {mana_cost} {power}\n"
                        # 修复：将 'manacost' 统一为 'mana_cost'
                        spell_info = {'type': spe_type, 'mana_cost': mana_cost, 'power': power}
                        
                        if actor_is_alive:
                            adv_learned_spells[actor_id][new_item_id] = spell_info
                            item_details[new_item_id] = spell_info
                
                # 如果指令无效（因为执行者死亡），则新生成的ID实际上未被使用，需要释放
                if new_item_id and not actor_is_alive:
                    used_ids.discard(new_item_id)
            
            # 移除物品
            elif op_type == "ri":
                # ... ri logic (same as before)
                owners = [adv for adv in existing_adv if adv_owned_items.get(adv)] 
                if not owners: continue

                if dead_adv and random.random() < PROB_USE_DEAD_ACTOR: 
                    actor_id = random.choice([adv for adv in dead_adv if adv_owned_items.get(adv)])
                else: 
                    actor_id = random.choice([adv for adv in living_adv if adv_owned_items.get(adv)])
                
                actor_is_alive = adv_attributes[actor_id]['hp'] > 0
                item_id_to_remove = random.choice(list(adv_owned_items[actor_id].keys())) 
                line = f"ri {actor_id} {item_id_to_remove}\n"
                
                if actor_is_alive:
                    item_category = get_item_category(item_id_to_remove)
                    del adv_owned_items[actor_id][item_id_to_remove]
                    
                    backpack = adv_backpacks.get(actor_id, {'bottles': [], 'sword': None, 'magicbook': None, 'armour': None})
                    
                    if item_category == ITEM_TYPE_BOTTLE:
                        if item_id_to_remove in backpack.get('bottles', []):
                            backpack['bottles'].remove(item_id_to_remove)
                    elif item_category == ITEM_TYPE_SWORD:
                        if backpack.get('sword') == item_id_to_remove:
                            backpack['sword'] = None
                    elif item_category == ITEM_TYPE_MAGICBOOK:
                        if backpack.get('magicbook') == item_id_to_remove:
                            backpack['magicbook'] = None
                    elif item_category == ITEM_TYPE_ARMOUR:
                        if backpack.get('armour') == item_id_to_remove:
                            backpack['armour'] = None
                    
                    if item_id_to_remove in item_details:
                        del item_details[item_id_to_remove]
            
            # 携带物品 (TI)
            elif op_type == "ti":
                def get_uncarried_items(adv_id):
                    owned_items = set(adv_owned_items.get(adv_id, {}).keys())
                    backpack = adv_backpacks.get(adv_id, {'bottles': [], 'sword': None, 'magicbook': None, 'armour': None})
                    carried_items = set()
                    carried_items.update(backpack.get('bottles', []))
                    if backpack.get('sword') is not None:
                        carried_items.add(backpack['sword'])
                    if backpack.get('magicbook') is not None:
                        carried_items.add(backpack['magicbook'])
                    if backpack.get('armour') is not None:
                        carried_items.add(backpack['armour'])
                    return owned_items - carried_items

                takers = [adv for adv in existing_adv if get_uncarried_items(adv)]
                if not takers: continue
                
                # 随机选择一个冒险者来执行 ti 操作
                takers_dead = [adv for adv in takers if adv in dead_adv]
                if takers_dead and random.random() < PROB_USE_DEAD_ACTOR: 
                    actor_id = random.choice(takers_dead)
                else: 
                    actor_id = random.choice(takers)

                actor_is_alive = adv_attributes[actor_id]['hp'] > 0
                uncarried_items = get_uncarried_items(actor_id) 
                item_id_to_take = random.choice(list(uncarried_items)) 
                line = f"ti {actor_id} {item_id_to_take}\n"
                
                if actor_is_alive:
                    item_category = get_item_category(item_id_to_take)
                    
                    if item_category == ITEM_TYPE_SWORD:
                        # 移除现有武器，分配新武器
                        remove_weapon_if_exists(actor_id)
                        adv_backpacks[actor_id]['sword'] = item_id_to_take
                        adv_backpacks[actor_id]['magicbook'] = None
                    elif item_category == ITEM_TYPE_MAGICBOOK:
                        # 移除现有武器，分配新武器
                        remove_weapon_if_exists(actor_id)
                        adv_backpacks[actor_id]['magicbook'] = item_id_to_take
                        adv_backpacks[actor_id]['sword'] = None
                    elif item_category == ITEM_TYPE_ARMOUR:
                        # 移除现有装甲，分配新装甲
                        remove_armour_if_exists(actor_id)
                        adv_backpacks[actor_id]['armour'] = item_id_to_take
                    elif item_category == ITEM_TYPE_BOTTLE:
                        bottles_list = adv_backpacks[actor_id]['bottles']
                        if len(bottles_list) >= BOTTLE_CAPACITY:
                            # 药水瓶满了，顶替最早的
                            discard_oldest_bottle(actor_id)
                        # 添加新的药水瓶 (新的药水瓶在列表末尾)
                        adv_backpacks[actor_id]['bottles'].append(item_id_to_take)
            
            # 购买物品 (BI)
            elif op_type == "bi":
                # ... bi actor selection (same as before)
                if dead_adv and random.random() < PROB_USE_DEAD_ACTOR: 
                    actor_id = random.choice(dead_adv)
                elif existing_adv: 
                    actor_id = random.choice(list(existing_adv))
                else: continue

                actor_is_alive = adv_attributes[actor_id]['hp'] > 0
                
                # 选择要购买的物品类型
                available_purchase_types = []
                if any(bot not in used_ids for bot in bottle_id_pool):
                    available_purchase_types.extend(["HpBottle", "AtkBottle", "DefBottle", "ManaBottle"])
                if any(equ not in used_ids for equ in sword_id_pool):
                    available_purchase_types.append("Sword")
                if any(equ not in used_ids for equ in magicbook_id_pool):
                    available_purchase_types.append("Magicbook")
                if any(equ not in used_ids for equ in armour_id_pool):
                    available_purchase_types.append("Armour")

                if not available_purchase_types: continue

                item_type = random.choice(available_purchase_types)

                # 计算消耗的金币数 (x = min(money, 100))
                current_money = adv_attributes[actor_id].get('money', 0)
                cost = min(current_money, 100)

                new_item_id = None

                # 根据消耗的金币数决定物品效果/属性
                if item_type in ["HpBottle", "AtkBottle", "DefBottle", "ManaBottle"]:
                    item_pool = bottle_id_pool
                    
                    new_item_id = get_unused_id(item_pool)
                    if new_item_id:
                        effect = cost  
                        line = f"bi {actor_id} {new_item_id} {item_type}\n"
                        
                        if actor_is_alive:
                            adv_attributes[actor_id]['money'] -= cost
                            adv_owned_items[actor_id][new_item_id] = item_type
                            item_details[new_item_id] = {'type': item_type, 'effect': effect}
                    
                else:  # 装备类型
                    if item_type == "Sword":
                        item_pool = sword_id_pool
                    elif item_type == "Magicbook":
                        item_pool = magicbook_id_pool
                    elif item_type == "Armour":
                        item_pool = armour_id_pool
                    
                    new_item_id = get_unused_id(item_pool)

                    if new_item_id:
                        line = f"bi {actor_id} {new_item_id} {item_type}\n"
                        ce = cost
                        
                        if actor_is_alive:
                            adv_attributes[actor_id]['money'] -= cost
                            adv_owned_items[actor_id][new_item_id] = item_type 
                            item_details[new_item_id] = {'type': item_type, 'ce': ce}

                if new_item_id and not actor_is_alive:
                    used_ids.discard(new_item_id)

            # 战斗指令
            elif op_type == "fight":
                # ... fight logic (updated to use new perform_battle)
                if not existing_adv: continue

                if dead_adv and random.random() < PROB_USE_DEAD_ACTOR:
                    attacker_id = random.choice(dead_adv)
                else:
                    attacker_id = random.choice(list(existing_adv))

                attacker_is_alive = adv_attributes[attacker_id]['hp'] > 0

                # 目标必须存在且全部存活，且不能包含攻击者自己
                alive_targets = [adv for adv in existing_adv if adv_attributes[adv]['hp'] > 0 and adv != attacker_id]
                if not alive_targets:
                    continue
                
                # 决定单目标或多目标
                if random.random() < 0.7 or len(alive_targets) < 3:
                    target_id = random.choice(alive_targets)
                    target_ids = [target_id]
                    line = f"fight {attacker_id} 1 {target_id}\n"
                else:
                    num_targets = min(random.randint(2, 30), len(alive_targets))
                    target_ids = random.sample(alive_targets, num_targets)
                    targets_str = " ".join(target_ids)
                    line = f"fight {attacker_id} {len(target_ids)} {targets_str}\n"

                # 执行战斗逻辑 (无论攻击者是否存活，都尝试生成并执行)
                success, _ = perform_battle(attacker_id, target_ids)
                
            # 使用物品/法术 (USE)
            elif op_type == "use":
                # 找到持有 *携带* 药水瓶或 *学会* 法术的冒险者
                users = []
                for adv in existing_adv:
                    carried_bottles = adv_backpacks.get(adv, {}).get('bottles', [])
                    has_learned_spell = bool(adv_learned_spells.get(adv))
                    if carried_bottles or has_learned_spell:
                        users.append(adv)
                if not users: continue
                
                if dead_adv and random.random() < PROB_USE_DEAD_ACTOR: 
                    actor_id = random.choice([adv for adv in users if adv in dead_adv])
                else: 
                    actor_id = random.choice(users)
                
                actor_is_alive = adv_attributes[actor_id]['hp'] > 0
                
                # 目标必须存在
                if not existing_adv: continue
                target_id = random.choice(list(existing_adv)) 
                target_is_alive = adv_attributes[target_id]['hp'] > 0

                # 选择一个物品或法术
                carried_bottles = adv_backpacks.get(actor_id, {}).get('bottles', [])
                learned_spells = list(adv_learned_spells.get(actor_id, {}).keys())

                usable_items = []
                if carried_bottles and learned_spells:
                    if random.random() < 0.7:
                        usable_items = carried_bottles
                    else:
                        usable_items = learned_spells
                elif carried_bottles:
                    usable_items = carried_bottles
                elif learned_spells:
                    usable_items = learned_spells
                
                if not usable_items: continue
                    
                usable_id = random.choice(usable_items) 
                line = f"use {actor_id} {usable_id} {target_id}\n"
                
                # 状态更新 (仅当执行者存活且目标存活时)
                if actor_is_alive and target_is_alive:
                    
                    is_spell = usable_id in adv_learned_spells.get(actor_id, {})
                    is_bottle = usable_id in adv_owned_items.get(actor_id, {}) and adv_owned_items[actor_id][usable_id] in bottle_types
                    bottle_is_taken = usable_id in adv_backpacks.get(actor_id, {}).get('bottles', [])

                    if is_spell and adv_attributes[actor_id]['mana'] >= item_details[usable_id].get('mana_cost', 999): # 统一使用 'mana_cost'
                        spell_info = item_details[usable_id]
                        adv_attributes[actor_id]['mana'] -= spell_info['mana_cost'] # 统一使用 'mana_cost'
                        if spell_info['type'] == 'HealSpell': 
                            adv_attributes[target_id]['hp'] += spell_info['power']
                        elif spell_info['type'] == 'AttackSpell':
                            adv_attributes[target_id]['hp'] -= spell_info['power']
                            if adv_attributes[target_id]['hp'] <= 0:
                                adv_attributes[target_id]['hp'] = 0
                                kill_gold = calculate_kill_gold(target_id, actor_id)
                                if kill_gold > 0:
                                    adv_attributes[actor_id]['money'] += kill_gold
                                    
                    elif is_bottle and bottle_is_taken: # 必须是携带的药水瓶
                        item_info = item_details[usable_id]
                        if item_info['type'] == 'HpBottle': adv_attributes[target_id]['hp'] += item_info['effect']
                        elif item_info['type'] == 'AtkBottle': adv_attributes[target_id]['atk'] += item_info['effect']
                        elif item_info['type'] == 'DefBottle': adv_attributes[target_id]['def'] += item_info['effect']
                        elif item_info['type'] == 'ManaBottle': adv_attributes[target_id]['mana'] += item_info['effect']
                        
                        # 药水消耗
                        del adv_owned_items[actor_id][usable_id]
                        if usable_id in adv_backpacks[actor_id]['bottles']:
                            adv_backpacks[actor_id]['bottles'].remove(usable_id)
                        del item_details[usable_id]

            if line:
                f_input.write(line)
                op_count += 1 # 修复：将 _ += 1 替换为 op_count += 1

    print(f"Test case {test_case_id} generated with {num_operations} operations.")


if __name__ == "__main__":
    # 请确保您的 id_pools.py 文件位于同一目录下
    # id_pools 中的ID应该与您的第三次作业保持一致
    for i in range(1, 4):
        generate_test_case(i, 2000)
