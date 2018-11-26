



execute if score fireworks_change funcs matches 0 run data merge block ~0 ~1 ~0 {Items:[{Slot:0,id:"minecraft:firework_rocket",Count:1,tag:{Fireworks:{Flight:0,Explosions:[{Type:0,Trail:1,Colors:[I;11743532]}]}}}]}


execute if score fireworks_change funcs matches 1 run data merge block ~0 ~1 ~0 {Items:[{Slot:0,id:"minecraft:firework_rocket",Count:1,tag:{Fireworks:{Flight:0,Explosions:[{Type:1,Trail:1,Colors:[I;6719955]}]}}}]}


execute if score fireworks_change funcs matches 2 run data merge block ~0 ~1 ~0 {Items:[{Slot:0,id:"minecraft:firework_rocket",Count:1,tag:{Fireworks:{Flight:0,Explosions:[{Type:2,Trail:1,Colors:[I;14602026]}]}}}]}


execute if score fireworks_change funcs matches 3 run data merge block ~0 ~1 ~0 {Items:[{Slot:0,id:"minecraft:firework_rocket",Count:1,tag:{Fireworks:{Flight:0,Explosions:[{Type:3,Trail:1,Colors:[I;3887386]}]}}}]}


execute if score fireworks_change funcs matches 4 run data merge block ~0 ~1 ~0 {Items:[{Slot:0,id:"minecraft:firework_rocket",Count:1,tag:{Fireworks:{Flight:0,Explosions:[{Type:4,Trail:1,Colors:[I;15790320]}]}}}]}


setblock ~ ~ ~ redstone_torch
setblock ~ ~ ~ air
