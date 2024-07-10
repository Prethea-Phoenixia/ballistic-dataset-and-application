"""
Jinpeng Zhai, 2024 07 02
914962409@qq.com
An example parser implemented in Python to read the artillery database and convert it
to object-oriented programming friendly object structure."""

from __future__ import annotations
from typing import Optional, Dict, Iterable, List
import json
from math import pi

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def deg_to_rad(deg: float) -> float:
    return deg * pi / 180


class Charge:
    """docstring for Charge"""

    def __init__(
        self,
        load: Load,
        name_en: str,
        name_cn: str,
        comment: str,
        charge_mass: float,
        charge_type: str,
        amount: int,
    ):
        self.load = load
        self.name_en = name_en
        self.name_cn = name_cn
        self.comment = comment
        self.charge_type = charge_type
        self.charge_mass = charge_mass
        self.amount = amount

    def __getattr__(self, item):
        return getattr(self.load, item)

    @staticmethod
    def from_dict(load: Load, d: Dict):
        try:
            charge_name_cn = d.get("name_cn", "主装药")
            charge_name_en = d.get("name_en", "Main Charge")
            charge_comment = d.get("comment", "")
            charge_type = d["charge_type"]
            charge_mass = d["charge_mass_kg"]
            charge_amount = d.get("amount", 1)
        except KeyError as e:
            logger.warning(f"failed to parse charge attribute : {e}")
            return

        charge = Charge(
            load=load,
            name_cn=charge_name_cn,
            name_en=charge_name_en,
            comment=charge_comment,
            charge_type=charge_type,
            charge_mass=charge_mass,
            amount=charge_amount,
        )

        load.add_charge(charge)

    def __str__(self) -> str:
        return str(self.load) + " / " + self.name_en


class Load:
    def __init__(
        self,
        shell: Shell,
        name_cn: str,
        name_en: str,
        muzzle_velocity: float,
        max_avg_pressure: Optional[float],
        comment: str,
        c_43: Optional[float],
        i_43: Optional[float],
    ):
        self.charges: List[Charge] = []
        self.name_cn = name_cn
        self.name_en = name_en
        self.muzzle_velocity = muzzle_velocity  # m/s
        self.comment = comment
        self.shell = shell  # parent

        if c_43:
            i_43 = i_43 or c_43 * self.shot_mass * 1e3 / (self.caliber**2)

        self.i_43 = i_43 or self.i_43

    def __getattr__(self, item):
        return getattr(self.shell, item)

    def __iter__(self) -> Iterable[Charge]:
        return iter(self.charges)

    @staticmethod
    def from_dict(shell: Shell, d: Dict):
        try:
            load_name_cn = d.get("name_cn", "正常装药")
            load_name_en = d.get("name_en", "Normal Charge")
            load_muzzle_velocity = d["muzzle_velocity_m/s"]
            load_max_avg_pressure = d.get("max_avg_pressure_kgf/sqcm")
            load_comment = d.get("comment", "")
            load_i_43 = d.get("i_43")
            load_c_43 = d.get("c_43")
            load_charges = d["charges"]

        except KeyError as e:
            logger.warning(f"failed to parse load attribute: {e}")
            return

        load = Load(
            shell=shell,
            name_cn=load_name_cn,
            name_en=load_name_en,
            muzzle_velocity=load_muzzle_velocity,
            max_avg_pressure=load_max_avg_pressure,
            comment=load_comment,
            i_43=load_i_43,
            c_43=load_c_43,
        )

        for charge_dict in load_charges:
            Charge.from_dict(load, charge_dict)

        if load.charges:
            shell.add_load(load)

    def __str__(self) -> str:
        return str(self.shell) + " / " + self.name_en

    def add_charge(self, charge: Charge):
        self.charges.append(charge)

    # def get_min_elev(self) -> Optional[float]:
    #     return self.shell.gun.min_elev

    # def get_max_elev(self) -> Optional[float]:
    #     return self.shell.gun.max_elev


class Shell:
    def __init__(
        self,
        gun: Gun,
        name_cn: str,
        name_en: str,
        shell_types: List[str],
        shot_mass: float,
        travel: Optional[float],
        chamber_length: Optional[float],
        chamber_volume: Optional[float],
        c_43: Optional[float],
        i_43: Optional[float],
        comment: str,
    ):

        self.gun = gun
        self.loads: List[Load] = []
        self.name_cn = name_cn
        self.name_en = name_en
        self.shell_types = shell_types
        self.shot_mass = shot_mass  # kg
        self.travel = travel
        self.chamber_volume = chamber_volume

        if c_43:
            i_43 = i_43 or c_43 * self.shot_mass * 1e3 / (self.caliber**2)
        self.i_43 = i_43

        self.comment = comment

    def __iter__(self) -> Iterable[Load]:
        return iter(self.loads)

    def __getattr__(self, item):
        return getattr(self.gun, item)

    def add_load(self, *loads: Load):
        self.loads.extend(loads)

    @staticmethod
    def from_dict(gun: Gun, d: Dict):
        try:
            shell_name_cn = d["name_cn"]
            shell_name_en = d["name_en"]
            shell_shot_mass = d["shot_mass_kg"]
            shell_types = [v.strip() for v in d["shell_types"].split(",")]
            shell_travel = d.get("travel_dm")
            shell_chamber_length = d.get("chamber_length_dm")
            shell_chamber_volume = d.get("chamber_volume_L")

            shell_i_43 = d.get("i_43")
            shell_c_43 = d.get("c_43")
            shell_loads = d["loads"]
            shell_comment = d.get("comment", "")  # nullable

        except KeyError as e:
            logger.warning(f"failed to parse shell attribute: {e}")
            return

        shell = Shell(
            gun=gun,
            name_cn=shell_name_cn,
            name_en=shell_name_en,
            shell_types=shell_types,
            shot_mass=shell_shot_mass,
            travel=shell_travel,
            chamber_length=shell_chamber_length,
            chamber_volume=shell_chamber_volume,
            i_43=shell_i_43,
            c_43=shell_c_43,
            comment=shell_comment,
        )

        for shell_dict in shell_loads:
            Load.from_dict(shell, shell_dict)

        if shell.loads:
            gun.add_shell(shell)

    def __str__(self) -> str:
        return str(self.gun) + " / " + self.name_en


class Gun:
    def __init__(
        self,
        name_cn: str,
        name_en: str,
        caliber: float,
        left_arc: Optional[float],
        right_arc: Optional[float],
        min_elev: Optional[float],
        max_elev: Optional[float],
        comment: str,
    ):
        self.shells: List[Shell] = []  # child

        self.name_cn = name_cn
        self.name_en = name_en
        self.caliber = caliber  # in mm
        self.left_arc = left_arc  # in degrees
        self.right_arc = right_arc  # in degrees
        self.min_elev = min_elev  # in degrees
        self.max_elev = max_elev  # in degrees
        self.comment = comment

    def __iter__(self) -> Iterable[Shell]:
        return iter(self.shells)

    def add_shell(self, *shells: Shell):
        self.shells.extend(shells)

    @staticmethod
    def from_dict(ext_bal: BallisticDB, d: Dict):
        try:
            gun_name_cn = d["name_cn"]
            gun_name_en = d["name_en"]
            gun_caliber = d["caliber_mm"]
            gun_shells = d["shells"]
            gun_comment = d.get("comment", "")
            gun_min_elev = d.get("min_elev_deg")
            gun_max_elev = d.get("max_elev_deg")

            gun_left_arc = d.get("firing_arc_left_deg")
            gun_right_arc = d.get("firing_arc_right_deg")

        except KeyError as e:
            logger.warning(f"failed to parse attribute at gun level: {e}")
            return

        gun = Gun(
            name_cn=gun_name_cn,
            name_en=gun_name_en,
            caliber=gun_caliber,
            left_arc=gun_left_arc,
            right_arc=gun_right_arc,
            min_elev=gun_min_elev,
            max_elev=gun_max_elev,
            comment=gun_comment,
        )

        for shell_dict in gun_shells:
            Shell.from_dict(gun, shell_dict)

        if gun.shells:
            ext_bal.add_gun(gun)

    def __str__(self) -> str:
        return self.name_en


class BallisticDB:

    def __init__(self, path: Optional[str]):
        logger.info(f"initiating db with file {path}")
        self.guns: List[Gun] = []

        if path:
            with open(path, mode="r", encoding="utf-8") as jsonfile:
                data = json.load(jsonfile)

            for gun_dict in data["guns"]:
                Gun.from_dict(self, gun_dict)

        logger.info(f"finished initialization with {len(self.guns)} guns")

    def __iter__(self):
        return iter(self.guns)

    def add_gun(self, gun: Gun):
        self.guns.append(gun)

    def describe(self) -> str:
        string = ""
        for gun in self:
            string += f"{gun.name_en}\n"
            for shell in gun:
                string += f"\t{shell.name_en}\n"
                for load in shell:
                    string += f"\t\t{load.name_en}\n"
                    for charge in load:
                        string += f"\t\t\t{charge.name_en}\n"
        return string


if __name__ == "__main__":
    bdb = BallisticDB("arty.json")
    print(bdb.describe())
