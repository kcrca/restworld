import os
import shutil

biome_table = {
    'Snowy': ('Snowy Tundra', 'Snowy Tiaga', 'Ice Spikes'),
    'Cold': ('Tiaga', 'Stone Shore'),
}


def main():
    # dir = os.path.dirname(__file__)
    # gen_dir = os.path.join(dir, 'generated')
    # shutil.rmtree(gen_dir)
    # os.makedirs(gen_dir, 0777)
    # os.chdir(gen_dir)
    for i, (group, biomes) in enumerate(biome_table.items()):
        tmpl = r"""
            <%%namespace file="../sign_base.mcftmpl" import="*"/>

            <%%def name='category_sign(category, x, biomes)'>
            setblock ~${x} ~1 ~9 oak_wall_sign{${sign_nbt(1, 'function v3:biomes/%%s_signs' %% category.lower(), category)},${sign_nbt(2, 'say hi %%s' %% category.lower(), "Biomes")}}
            </%%def>
            
            fill ~9 ~2 ~9 ~0 ~2 ~9 air
            ${category_sign('%s', %d, %s)}

            """ % (group, 9 - i, biomes)
        print tmpl
        # open('%s.mcftmpl' % group, 'w').write(
        #     tmpl
        # )



if __name__ == '__main__':
    main()
