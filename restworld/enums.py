from enum import Enum


class ValueEnum(Enum):
    def __str__(self):
        return super().value




class Advancement(ValueEnum):
    MINECRAFT = "story/root"
    """The heart and story of the game."""
    STONE_AGE = "story/mine_stone"
    """Mine stone with your new pickaxe."""
    GETTING_AN_UPGRADE = "story/upgrade_tools"
    """Construct a better pickaxe."""
    ACQUIRE_HARDWARE = "story/smelt_iron"
    """Smelt an iron ingot."""
    SUIT_UP = "story/obtain_armor"
    """Protect yourself with a piece of iron armor."""
    HOT_STUFF = "story/lava_bucket"
    """Fill a bucket with lava."""
    ISNT_IT_IRON_PICK = "story/iron_tools"
    """Upgrade your pickaxe."""
    NOT_TODAY_THANK_YOU = "story/deflect_arrow"
    """Block a projectile using your shield."""
    ICE_BUCKET_CHALLENGE = "story/form_obsidian"
    """Obtain a block of obsidian."""
    DIAMONDS = "story/mine_diamond"
    """Acquire diamonds."""
    WE_NEED_TO_GO_DEEPER = "story/enter_the_nether"
    """Build, light and enter a Nether Portal."""
    COVER_ME_WITH_DIAMONDS = "story/shiny_gear"
    """Diamond armor saves lives."""
    ENCHANTER = "story/enchant_item"
    """Enchant an item at an Enchantment Table."""
    ZOMBIE_DOCTOR = "story/cure_zombie_villager"
    """Weaken and then cure a Zombie Villager."""
    EYE_SPY = "story/follow_ender_eye"
    """Follow an Ender Eye."""
    ENTER_THE_END = "story/enter_the_end"
    """Enter the End Portal."""
    NETHER = "nether/root"
    """Bring summer clothes."""
    RETURN_TO_SENDER = "nether/return_to_sender"
    """Destroy a Ghast with a fireball."""
    THOSE_WERE_THE_DAYS = "nether/find_bastion"
    """Enter a Bastion Remnant."""
    HIDDEN_IN_THE_DEPTHS = "nether/obtain_ancient_debris"
    """Obtain Ancient Debris."""
    SUBSPACE_BUBBLE = "nether/fast_travel"
    """Use the Nether to travel 7 km in the Overworld."""
    A_TERRIBLE_FORTRESS = "nether/find_fortress"
    """Break your way into a Nether Fortress."""
    WHO_IS_CUTTING_ONIONS = "nether/obtain_crying_obsidian"
    """Obtain Crying Obsidian."""
    OH_SHINY = "nether/distract_piglin"
    """Distract Piglins with gold."""
    THIS_BOAT_HAS_LEGS = "nether/ride_strider"
    """Ride a Strider with a Warped Fungus on a Stick."""
    UNEASY_ALLIANCE = "nether/uneasy_alliance"
    """Rescue a Ghast from the Nether, bring it safely home to the Overworld... and then kill it."""
    WAR_PIGS = "nether/loot_bastion"
    """Loot a chest in a Bastion Remnant."""
    COUNTRY_LODE_TAKE_ME_HOME = "nether/use_lodestone"
    """Use a compass on a Lodestone."""
    COVER_ME_IN_DEBRIS = "nether/netherite_armor"
    """Get a full suit of Netherite armor."""
    SPOOKY_SCARY_SKELETON = "nether/get_wither_skull"
    """Obtain a Wither Skeleton's skull."""
    INTO_FIRE = "nether/obtain_blaze_rod"
    """Relieve a Blaze of its rod."""
    NOT_QUITE_NINE_LIVES = "nether/charge_respawn_anchor"
    """Charge a Respawn Anchor to the maximum."""
    FEELS_LIKE_HOME = "nether/ride_strider_in_overworld_lava"
    """Take a Strider for a loooong ride on a lava lake in the Overworld."""
    HOT_TOURIST_DESTINATIONS = "nether/explore_nether"
    """Explore all Nether biomes."""
    WITHERING_HEIGHTS = "nether/summon_wither"
    """Summon the Wither."""
    LOCAL_BREWERY = "nether/brew_potion"
    """Brew a potion."""
    BRING_HOME_THE_BEACON = "nether/create_beacon"
    """Construct and place a beacon."""
    A_FURIOUS_COCKTAIL = "nether/all_potions"
    """Have every potion effect applied at the same time."""
    BEACONATOR = "nether/create_full_beacon"
    """Bring a beacon to full power."""
    HOW_DID_WE_GET_HERE = "nether/all_effects"
    """Have every effect applied at the same time."""
    THE_END = "end/root"
    """Or the beginning?"""
    FREE_THE_END = "end/kill_dragon"
    """Good luck."""
    THE_NEXT_GENERATION = "end/dragon_egg"
    """Hold the Dragon Egg."""
    REMOTE_GETAWAY = "end/enter_end_gateway"
    """Escape the island."""
    THE_END_AGAIN = "end/respawn_dragon"
    """Respawn the Ender Dragon."""
    YOU_NEED_A_MINT = "end/dragon_breath"
    """Collect dragon's breath in a glass bottle."""
    THE_CITY_AT_THE_END_OF_THE_GAME = "end/find_end_city"
    """Go on in, what could happen?"""
    SKYS_THE_LIMIT = "end/elytra"
    """Find elytra."""
    GREAT_VIEW_FROM_UP_HERE = "end/levitate"
    """Levitate up 50 blocks from the attacks of a Shulker."""
    ADVENTURE = "adventure/root"
    """Adventure, exploration, and combat."""
    VOLUNTARY_EXILE = "adventure/voluntary_exile"
    """Kill a raid captain.Maybe consider staying away from villages for the time being..."""
    IS_IT_A_BIRD = "adventure/spyglass_at_parrot"
    """Look at a parrot through a spyglass."""
    MONSTER_HUNTER = "adventure/kill_a_mob"
    """Kill any hostile monster."""
    WHAT_A_DEAL = "adventure/trade"
    """Successfully trade with a Villager."""
    STICKY_SITUATION = "adventure/honey_block_slide"
    """Jump into a Honey Block to break your fall."""
    OL_BETSY = "adventure/ol_betsy"
    """Shoot a crossbow."""
    SURGE_PROTECTOR = "adventure/lightning_rod_with_villager_no_fire"
    """Protect a villager from an undesired shock without starting a fire."""
    CAVES__CLIFFS = "adventure/fall_from_world_height"
    """Free fall from the top of the world (build limit) to the bottom of the world and survive."""
    SNEAK_100 = "adventure/avoid_vibration"
    """Sneak near a Sculk Sensor or Warden to prevent it from detecting you‌."""
    SWEET_DREAMS = "adventure/sleep_in_bed"
    """Sleep in a bed to change your respawn point."""
    HERO_OF_THE_VILLAGE = "adventure/hero_of_the_village"
    """Successfully defend a village from a raid."""
    IS_IT_A_BALLOON = "adventure/spyglass_at_ghast"
    """Look at a ghast through a spyglass."""
    A_THROWAWAY_JOKE = "adventure/throw_trident"
    """Throw a trident at something.Note: Throwing away your only weapon is not a good idea."""
    IT_SPREADS = "adventure/kill_mob_near_sculk_catalyst"
    """Kill a mob near a Sculk Catalyst‌."""
    TAKE_AIM = "adventure/shoot_arrow"
    """Shoot something with an arrow."""
    MONSTERS_HUNTED = "adventure/kill_all_mobs"
    """Kill one of every hostile monster."""
    POSTMORTAL = "adventure/totem_of_undying"
    """Use a Totem of Undying to cheat death."""
    HIRED_HELP = "adventure/summon_iron_golem"
    """Summon an Iron Golem to help defend a village."""
    STAR_TRADER = "adventure/trade_at_world_height"
    """Trade with a Villager at the build height limit."""
    TWO_BIRDS_ONE_ARROW = "adventure/two_birds_one_arrow"
    """Kill two Phantoms with a piercing arrow."""
    WHOS_THE_PILLAGER_NOW = "adventure/whos_the_pillager_now"
    """Give a Pillager a taste of their own medicine."""
    ARBALISTIC = "adventure/arbalistic"
    """Kill five unique mobs with one crossbow shot."""
    ADVENTURING_TIME = "adventure/adventuring_time"
    """Discover every biome."""
    SOUND_OF_MUSIC = "adventure/play_jukebox_in_meadows"
    """Make the Meadows come alive with the sound of music from a Jukebox."""
    LIGHT_AS_A_RABBIT = "adventure/walk_on_powder_snow_with_leather_boots"
    """Walk on powder snow...without sinking in it."""
    IS_IT_A_PLANE = "adventure/spyglass_at_dragon"
    """Look at the Ender Dragon through a spyglass."""
    VERY_VERY_FRIGHTENING = "adventure/very_very_frightening"
    """Strike a Villager with lightning."""
    SNIPER_DUEL = "adventure/sniper_duel"
    """Kill a Skeleton from at least 50 meters away."""
    BULLSEYE = "adventure/bullseye"
    """Hit the bullseye of a Target block from at least 30 meters away."""
    HUSBANDRY = "husbandry/root"
    """The world is full of friends and food."""
    BEE_OUR_GUEST = "husbandry/safely_harvest_honey"
    """Use a Campfire to collect Honey from a Beehive using a Bottle without aggravating the bees."""
    THE_PARROTS_AND_THE_BATS = "husbandry/breed_an_animal"
    """Breed two animals together."""
    YOUVE_GOT_A_FRIEND_IN_ME = "husbandry/allay_deliver_item_to_player"
    """Have an Allay deliver items to you‌."""
    WHATEVER_FLOATS_YOUR_GOAT = "husbandry/ride_a_boat_with_a_goat"
    """Get in a Boat and float with a Goat."""
    BEST_FRIENDS_FOREVER = "husbandry/tame_an_animal"
    """Tame an animal."""
    GLOW_AND_BEHOLD = "husbandry/make_a_sign_glow"
    """Make the text of a sign glow."""
    FISHY_BUSINESS = "husbandry/fishy_business"
    """Catch a fish."""
    TOTAL_BEELOCATION = "husbandry/silk_touch_nest"
    """Move a Bee Nest, with 3 bees inside, using Silk Touch."""
    BUKKIT_BUKKIT = "husbandry/tadpole_in_a_bucket"
    """Catch a Tadpole in a Bucket‌."""
    A_SEEDY_PLACE = "husbandry/plant_seed"
    """Plant a seed and watch it grow."""
    WAX_ON = "husbandry/wax_on"
    """Apply Honeycomb to a Copper block!"""
    TWO_BY_TWO = "husbandry/bred_all_animals"
    """Breed all the animals!"""
    BIRTHDAY_SONG = "husbandry/allay_deliver_cake_to_note_block"
    """Have an Allay drop a Cake at a Note Block‌."""
    A_COMPLETE_CATALOGUE = "husbandry/complete_catalogue"
    """Tame all cat variants!"""
    TACTICAL_FISHING = "husbandry/tactical_fishing"
    """Catch a fish... without a fishing rod!"""
    WHEN_THE_SQUAD_HOPS_INTO_TOWN = "husbandry/leash_all_frog_variants"
    """Get each Frog variant on a Lead‌."""
    A_BALANCED_DIET = "husbandry/balanced_diet"
    """Eat everything that is edible, even if it's not good for you."""
    SERIOUS_DEDICATION = "husbandry/obtain_netherite_hoe"
    """Use a Netherite Ingot to upgrade a hoe, and then reevaluate your life choices."""
    WAX_OFF = "husbandry/wax_off"
    """Scrape Wax off of a Copper block!"""
    THE_CUTEST_PREDATOR = "husbandry/axolotl_in_a_bucket"
    """Catch an axolotl in a bucket."""
    WITH_OUR_POWERS_COMBINED = "husbandry/froglights"
    """Have all Froglights in your inventory‌."""
    THE_HEALING_POWER_OF_FRIENDSHIP = "husbandry/kill_axolotl_target"
    """Team up with an axolotl and win a fight."""