#!/bin/sh
sed -e 's/blocks*/stairs/' -e 's/planks/stairs/' -e 's/bricks/brick_stairs/' -e 's/stone"/stone_stairs"/' -e 's/marine"/marine_stairs"/' -e 's/ite"/ite_stairs"/' -e 's/_quartz"/_quartz_stairs"/' < stepable_planks.json > stepable_stairs.json
sed -e 's/stairs/slab/' < stepable_stairs.json > stepable_slabs.json
