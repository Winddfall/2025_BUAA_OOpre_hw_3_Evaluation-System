spell_id_pool = [
    # 原有法术扩展
    "Fireball", "Heal", "IceLance", "Thunderclap", "ShadowBolt", "HolyLight",
    "ArcaneMissile", "Rejuvenate", "ChainLightning", "DrainLife", "FrostNova",
    "EarthShield", "Sunfire", "Moonbeam", "Starfall",
    
    # 元素类法术 - 火
    "FireBolt", "FlameStrike", "FireShield", "Inferno", "Incinerate", "FlameWave",
    "FireballBarrage", "Ignite", "Scorch", "SearingRay", "Firestorm", "MoltenBlast",
    "Blaze", "EmberShower", "PhoenixFlame",
    "Cauterize", "Wildfire", "FlameWard", "AshCloud", "LavaFlow",
    "FireJet", "Burnout", "FurnaceBlast", "Kindle", "Pyroblast",
    "Combustion", "MagmaEruption", "HeatWave", "FireAura", "Dragon'sBreath",
    
    # 元素类法术 - 水/冰
    "FrostBolt", "IceStorm", "FrostArmor", "Freeze", "IceBarrier", "Blizzard",
    "Hailstorm", "Frostbite", "ChillTouch", "Glacier", "IceSpike", "FrostWave",
    "SleetStorm", "Permafrost", "AquaJet",
    "WaterWhip", "TidalWave", "FrostLance", "IceSpear", "Snowstorm",
    "IcyGrasp", "FrostNova", "FrozenOrb", "MistForm", "Drown",
    "WaterBreathing", "Tsunami", "HailBarrage", "FrostWard", "Crystalize",
    
    # 元素类法术 - 雷/电
    "LightningBolt", "Thunderstorm", "Electrocute", "Shock", "LightningShield",
    "ThunderWave", "StormSurge", "StaticCharge", "LightningArc", "ElectricNova",
    "ThunderClap", "BoltOfLightning", "EnergyBlast", "PlasmaBall", "ShockingGrasp",
    "Thunderbolt", "LightningChain", "ElectricalAura", "StormShield", "BallLightning",
    "ThunderousRoar", "ElectrostaticField", "LightningBlast", "Jolt", "TeslaCoil",
    "LightningStorm", "ThunderShield", "ElectricArmor", "Charge", "StormCall",
    
    # 元素类法术 - 土/自然
    "Earthquake", "RockSlide", "VineGrasp", "ThornWhip", "Nature'sBloom", "RootBind",
    "StoneSkin", "MudSlide", "Barkskin", "Regrowth", "Sprout", "WildGrowth", "EarthBolt",
    "CrystalSpike", "Nature'sWrath",
    "Entangle", "RockShield", "EarthenGrip", "MossCover", "BramblePatch",
    "Quicksand", "CrystalForest", "Mountain'sWrath", "RootNetwork", "ThornBarrier",
    "Nature'sBlessing", "GrowthSurge", "FungalInfestation", "InsectSwarm", "VenomousSting",
    "VineLash", "SeedBomb", "WoodenGolem", "RockGolem", "EarthPrison",
    
    # 神圣/光明类法术
    "HolySmite", "DivineProtection", "Bless", "Purify", "Resurrect", "HolyAura",
    "GuardianAngel", "LightOfDivinity", "SacredShield", "DivineIntervention",
    "HolyNova", "BlessedStrike", "Radiance", "Illumination", "HeavenlyLight",
    "HolyBolt", "DivineShield", "BlessedAura", "LightBlast", "Purification",
    "DivineFavor", "HolyRetribution", "AngelicGuardian", "LuminousShield", "Sanctify",
    "HallowedGround", "DivineHealing", "HolyWard", "SacredFlame", "RighteousSmite",
    "CelestialBlessing", "AngelicWings", "DivineWrath", "LightWell", "Halo",
    
    # 暗影/亡灵类法术
    "ShadowBall", "Darkness", "Curse", "Hex", "NecroticBolt", "ShadowForm",
    "RaiseDead", "DrainSoul", "VampiricTouch", "DarkPact", "ShadowStep", "UnholyFrenzy",
    "SoulReaper", "Plague", "DarknessEmbrace",
    "ShadowBoltVolley", "UnholyAura", "NecroticPlague", "VampiricEmbrace", "DarknessWave",
    "SoulDrain", "RaiseSkeleton", "SummonZombie", "Boneyard", "CarrionSwarm",
    "UnholyBolt", "ShadowShield", "DemonSummon", "FelFire", "SoulFire",
    "DarkCommand", "MindRot", "CorpseExplosion", "UnholyStrength", "ShadowCloak",
    "NecromanticAura", "LichForm", "VampireLord", "DarkRitual", "SoulPrison",
    
    # Arcane/魔法类法术
    "MagicMissile", "ArcaneExplosion", "Teleport", "Invisibility", "ManaShield",
    "Polymorph", "Counterspell", "ArcaneBarrage", "MagicWeapon", "SpellPower",
    "ArcaneIntellect", "ManaBurn", "SummonFamiliar", "ConjureFood", "ArcanePrison",
    "ArcaneBolt", "MagicShield", "Telekinesis", "ManaLeak", "SpellSteal",
    "ArcaneMissiles", "MagicBarrier", "TeleportationCircle", "InvisibleSphere", "ManaRegen",
    "ArcaneVortex", "MagicNegation", "CounterMagic", "ArcanePower", "SpellReflection",
    "ConjureWater", "SummonElemental", "MagicArmor", "ArcaneGuardian", "ManaBomb",
    "ArcaneExplosion", "TelepathicLink", "MagicDetection", "ArcaneEye", "SpellBreach",
    
    # 精神/心灵类法术
    "MindControl", "Telepathy", "Fear", "Charm", "Sleep", "Confusion",
    "CalmEmotions", "MindBlast", "PsychicScream", "Telekinesis", "Clairvoyance",
    "Premonition", "MentalShield", "ThoughtShield", "PsychicLink",
    "MindReading", "EmotionControl", "Hallucination", "PhobiaInducement", "CalmMind",
    "MentalBreak", "PsychicBarrier", "TelepathicBond", "MindWipe", "MemoryExtract",
    "ThoughtProjection", "MentalSuggestion", "Empathy", "MindHeal", "PsychicAssault",
    "EmotionSiphon", "FearAura", "CalmAura", "MindShackle", "TelepathicCommand",
    "MentalStrength", "PsychicShield", "MemoryAlter", "ThoughtSteal", "MindMeld"
]
bottle_id_pool = [
    # 原有药水扩展
    "HealPotion", "ManaPotion", "SpeedPotion", "StrengthPotion", "DexterityPotion",
    "ElixirOfLife", "Mageblood", "Swiftbrew", "Titan'sTonic", "ShadowDraught",
    "GlimmerleafAura", "DragonbreathSerum", "FrostfireExtract", "SoulEssence", "Witch'sBane",
    
    # 治疗类药水
    "VitalityVial", "RegenerationElixir", "WoundWash", "LifeforceLotion", "HeartmendDraught",
    "RejuvenationPotion", "BloodbindTincture", "AnimaElixir", "ScarlessSalve", "VigorVineExtract",
    "PulsePotion", "LifegivingLiqueur", "ReviveDew", "HealthHoney", "VitalizingVodka",
    "CureAllConcoction", "HealingHaze", "MendMead", "LifebloomBrew", "RestorativeRum",
    "CellRegenTonic", "TraumaTonic", "ScarFadeSolution", "VitalSpiritSip", "PulseRestorePotion",
    "WoundWeaveElixir", "BoneBondBalm", "MuscleMendMist", "OrganOintment", "NerveNurseNectar",
    "BloodBoostBeverage", "FleshFixFluid", "AuraHealAmpoule", "SpiritSootheSip", "VitalityVortexVial",
    
    # 魔法类药水
    "ArcaneAmbrose", "Wizard'sWine", "ManaMead", "Spellcaster'sSip", "Enchanter'sElixir",
    "MagickaMarmalade", "Sorcerer'sSap", "WandWash", "MysticMead", "CharmChaser",
    "Conjurer'sCordial", "HexHoney", "IncantationInfusion", "MagicMilk", "RuneRum",
    "SorcerySyrup", "Witch'sWort", "Wizard'sWellwater", "MysteryMead", "EnchantmentElixir",
    "ArcaneAmpoule", "ManaMist", "SpellSip", "CharmChaser", "Wizard'sWash",
    "MagicMist", "EnchantElixir", "SorcerySoda", "ConjureConcoction", "RuneRefresh",
    "MysticMist", "Witch'sWash", "Wizard'sWard", "ArcaneAura", "MagickaMist",
    
    # 属性增强类药水
    "BrawnBrew", "CunningConcoction", "DexterityDew", "EnduranceElixir", "FocusFluid",
    "GuileGrog", "HardinessHooch", "IntellectInfusion", "JudgmentJuice", "KeennessKoolaid",
    "LuckLiquor", "MightMead", "NimblenessNectar", "ObservantOil", "PowerPotion",
    "QuicknessQuaff", "ResolveRum", "StrengthSuds", "ToughnessTonic", "VigorVodka",
    "AgilityAmpoule", "BraveryBrew", "ClevernessCordial", "DiligenceDraught", "EnergyElixir",
    "FortitudeFluid", "GritGrog", "HasteHoney", "IntuitionInfusion", "JuggernautJuice",
    "KnowledgeKombucha", "LeadershipLiqueur", "MentalMightMead", "NimbleNectar", "OversightOil",
    
    # 特殊效果药水
    "InvisibilityInfusion", "LevitationLiqueur", "FireResistFizz", "FrostFendFizz",
    "ShockShieldSoda", "PoisonProofPotion", "FearlessFlask", "NightVisionNectar",
    "WaterBreathingWine", "FlightPotion", "TeleportTonic", "ShapeShiftSyrup",
    "TimeTwistTincture", "IllusionElixir", "SummoningSap", "BanishBrew", "CurseCureConcoction",
    "BlessedBeverage", "HolyHoney", "Demon'sDreadDrink", "Angel'sAmbrosia", "Dragon'sDraught",
    "PhoenixPotion", "UnicornUrine", "GriffinGrog", "MermaidMead", "SphinxSpirit",
    "KrakenKoolaid", "HydraHooch", "ChimeraCordial", "WyvernWine", "BeholderBrew",
    
    # 新增特殊效果药水
    "GhostformGrog", "GiantGrowthGuzzle", "ShrinkSerum", "PhasingPotion", "EtherealElixir",
    "DetectMagicDew", "TrueSightTonic", "MagicResistRum", "CurseCastingConcoction", "BlessingBrew",
    "SummonSteedSip", "MinionMead", "ElementalEssence", "WeatherWardWine", "EarthquakeElixir",
    "StormSip", "SunshineSoda", "MoonlightMead", "StarshineSyrup", "VoidVodka",
    "LightLiqueur", "DarkDraught", "SoundlessSip", "SilenceSolution", "EchoElixir",
    "TelepathyTonic", "MindShieldMead", "CharmResistRum", "FearFendFluid", "IllusionImmunityInfusion",
    "TimeSlowTincture", "HasteHooch", "RegrowLimbLotion", "UndeadUnholyUrn", "HolyBlessingBalm",
    "DemonDetectionDraught", "AngelAllureAmpoule", "DragonDreadDew", "FaeFriendFizz", "DwarfDelightDram",
    "ElfEaseElixir", "OrcOomphOil", "TrollToughTonic", "GoblinGleeGrog", "KoboldKickKoolaid",
    "GiantsGrowGuzzle", "DragonfireDefenseDew", "LycanthropyLotion", "VampirismVodka", "FeyFrenzyFluid",
    "ElementalFormElixir", "MetamorphosisMead", "PolymorphPotion", "ShapeShiftSyrup", "DisguiseDew",
    "CamouflageConcoction", "StealthSip", "AmbushAmpoule", "Assassin'sElixir", "SpySyrup",
    "Scout'sSolution", "Ranger'sRefresh", "Tracker'sTonic", "Hunter'sHooch", "Predator'sPotion",
    "PreyProtectionPotion", "HerbHunterHelper", "Miner'sMightMead", "Smith'sStrengthSip", "Crafter'sCordial",
    "Merchant'sMuseMead", "Bard'sBoostBeverage", "Cleric'sBlessingBrew", "Fighter'sFortitudeFluid", "Rogue'sRuseRum",
    "Wizard'sWisdomWine", "Warlock'sWitWash", "Paladin'sPurityPotion", "Ranger'sResilienceRefresh", "Monk'sMentalMead"
]
adventurer_id_pool = [
        # 原有人名扩展
        "Alice", "Bob", "Charlie", "Dave", "Eve", "Frank", "Grace",
        "Maximus", "Seraphina", "Kaelen", "Lyra", "Orion", "Thorn",
        "Zephyr", "Isolde", "Corvus", "Ember", "Finnian", "Rowan",
        
        # 新增人名 - 传统风格
        "Arthur", "Brianna", "Cedric", "Daphne", "Eldric", "Fiona", "Gavin",
        "Hilda", "Igor", "Jasmine", "Kyle", "Lila", "Marius", "Nora", "Owen",
        "Penelope", "Quentin", "Rosalind", "Silas", "Tabitha", "Ulysses", "Vera",
        "Warren", "Xena", "Yannick", "Zara", "Alaric", "Bianca", "Casper", "Diana",
        "Ewan", "Freya", "Gideon", "Hannah", "Ivan", "Jade", "Kara", "Leland",
        "Maya", "Nico", "Ophelia", "Percy", "Quinn", "Roland", "Sage", "Tobias",
        
        # 新增人名 - 奇幻风格
        "Aelar", "Bree", "Corin", "Dara", "Eldar", "Faelon", "Gimble",
        "Hilda", "Ithilwen", "Jorndan", "Kael", "Lirael", "Mordecai", "Nerys",
        "Oona", "Phelan", "Qara", "Riona", "Soren", "Tahlia", "Uthar", "Vex",
        "Wren", "Xan", "Yasha", "Zedd", "Arwen", "Borin", "Calen", "Drizzt",
        "Elara", "Fenrir", "Gimli", "Hilda", "Inigo", "Jynx", "Kili", "Luna",
        "Mordred", "Nyx", "Odin", "Pandora", "Questor", "Raven", "Sable", "Thorne",
        
        # 新增人名 - 异域风格
        "Akira", "Bao", "Chiyo", "Dai", "Emiko", "Fujin", "Goro",
        "Hana", "Ichiro", "Jun", "Kimi", "Ling", "Mako", "Nori", "Osamu",
        "Ping", "Qiu", "Ryo", "Sato", "Takeshi", "Uma", "Vinh", "Wei",
        "Xiao", "Yuki", "Zhen", "Aziz", "Banu", "Cem", "Dilara", "Ehsan",
        "Farid", "Gul", "Hakan", "Iman", "Jalal", "Kamal", "Laleh", "Mehmet",
        "Nadia", "Omar", "Parisa", "Qasim", "Rana", "Sami", "Tara", "Umar",
        "Vera", "Waleed", "Xanthe", "Yusuf", "Zara", "Aiden", "Brynn", "Cora",
        "Dex", "Elio", "Flora", "Grey", "Hugo", "Iris", "Jax", "Kai"
    ]
print(len(spell_id_pool))
print(len(bottle_id_pool))
print(len(adventurer_id_pool))