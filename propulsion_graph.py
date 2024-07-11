from __future__ import annotations
from ballistic_parser import BallisticDB

from matplotlib import pyplot as plt
from labellines import labelLine, labelLines
from scipy.spatial import ConvexHull
import scipy.interpolate
import numpy as np
from itertools import cycle


if __name__ == "__main__":

    bdb = BallisticDB("arty.json")
    print(bdb.describe())

    fig, ax = plt.subplots(figsize=(16, 9), layout="constrained")

    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = cycle(prop_cycle.by_key()["color"])
    marker_dict = {
        "AB": "<",
        "Frag": "x",
        "HE-Frag": "+",
        "HESH": "|",
        "AP": ">",
        "HEAT": "_",
        "Smoke": "o",
        "Illumination": "*",
        "Leaflet": "s",
    }

    for gun in bdb:

        color = next(colors)

        wmss, vss = [], []
        # points = []
        for shot in gun:

            for kw, marker in marker_dict.items():
                if kw in shot.shell_types:
                    break

            wms = [
                sum(charge.charge_mass * charge.amount for charge in load)
                / shot.shot_mass
                for load in shot
            ]
            vs = [load.muzzle_velocity for load in shot]
            wmss.extend(wms)
            vss.extend(vs)
            p = ax.scatter(
                wms,
                vs,
                alpha=0.66,
                c=color,
                marker=marker,
                s=16,
                label=gun.name_en + " " + shot.name_en,
            )
            # points.extend(zip(wms, vs))

        # if len(points) > 1:
        #     hull = ConvexHull(points)

        #     ax.fill(
        #         [wmss[v] for v in hull.vertices],
        #         [vss[v] for v in hull.vertices],
        #         c=color,
        #         alpha=0.33,
        #         linewidth=0,
        #         edgecolor=color,
        #     )

    ax.legend(loc="lower right", fontsize="xx-small", ncol=2)
    # ax.legend(loc="upper left", fontsize="small")

    ax.set_xlabel("charge to shot mass ratio")
    ax.set_ylabel("velocity m/s")

    ax.set_xlim(0, None)
    ax.set_ylim(0, None)

    # plt.show()
    plt.savefig("propulsion_graph")
