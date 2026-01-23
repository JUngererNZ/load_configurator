import math
from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

# ---------- domain models ----------

@dataclass
class Item:
    order: str
    consignment: str
    mass: float
    length: float
    width: float
    height: float
    rotatable: bool = True   # allow 90° rotation in plan view by default

    def orientations(self):
        """
        For now we only care about 'length' along the trailer.
        If rotatable, you may swap length/width.
        """
        if self.rotatable:
            return [
                {"name": "normal", "length": self.length, "width": self.width},
                {"name": "rotated", "length": self.width, "width": self.length},
            ]
        else:
            return [
                {"name": "normal", "length": self.length, "width": self.width},
            ]


@dataclass
class PlacedItem:
    item: Item
    orientation: str
    x_start: float
    x_end: float


@dataclass
class TrailerType:
    name: str
    deck_length: float       # metres
    max_mass: float          # tonnes or whatever unit matches 'mass'


@dataclass
class TrailerLoad:
    trailer_type: TrailerType
    index: int
    placed_items: List[PlacedItem] = field(default_factory=list)
    used_length: float = 0.0
    used_mass: float = 0.0

    def can_place(self, item: Item, orientation_len: float, gap: float = 0.0) -> bool:
        """Check if item fits in remaining length and mass."""
        length_needed = self.used_length + gap + orientation_len
        if length_needed > self.trailer_type.deck_length + 1e-6:
            return False
        if self.used_mass + item.mass > self.trailer_type.max_mass + 1e-6:
            return False
        return True

    def place(self, item: Item, orientation_name: str, orientation_len: float, gap: float = 0.0):
        x_start = self.used_length + gap
        x_end = x_start + orientation_len
        self.placed_items.append(
            PlacedItem(
                item=item,
                orientation=orientation_name,
                x_start=x_start,
                x_end=x_end,
            )
        )
        self.used_length = x_end
        self.used_mass += item.mass


# ---------- core algorithm ----------

def load_items_to_trailers(
    items: List[Item],
    trailer_types: List[TrailerType],
    trailer_count: int,
    gap: float = 0.0,
) -> List[TrailerLoad]:
    """
    Simple greedy heuristic:
    - Sort items by descending length (longest first).
    - Try to place each item in the first trailer where it fits
      (checking possible orientations).
    """
    # sort longest first
    items_sorted = sorted(items, key=lambda i: i.length, reverse=True)

    # create trailers (for now, fixed type sequence)
    loads: List[TrailerLoad] = []
    for i in range(trailer_count):
        t_type = trailer_types[min(i, len(trailer_types) - 1)]
        loads.append(TrailerLoad(trailer_type=t_type, index=i + 1))

    for item in items_sorted:
        placed = False
        for load in loads:
            for ori in item.orientations():
                if load.can_place(item, ori["length"], gap=gap):
                    load.place(item, ori["name"], ori["length"], gap=gap)
                    placed = True
                    break
            if placed:
                break
        if not placed:
            print(f"WARNING: item {item.order} ({item.consignment}) did not fit in any trailer")
    return loads


# ---------- helper: read your Excel sheet ----------

def read_items_from_excel(path: str) -> List[Item]:
    """
    Assumes structure like your sample:
    ORDER NUMBER in one column, CONSIGNMENT, MASS, LENGTH, WIDTH, HEIGHT. [file:5]
    Adjust column names/indexes to match your real file.
    """
    df = pd.read_excel(path, sheet_name=0, header=None)

    # locate the header row that contains 'ORDER NUMBER'
    header_row = None
    for i, row in df.iterrows():
        if (row == "ORDER NUMBER").any():
            header_row = i
            break
    if header_row is None:
        raise ValueError("Could not find 'ORDER NUMBER' header row")

    df2 = pd.read_excel(path, sheet_name=0, header=header_row)

    # keep only the key columns present in your file [file:5]
    cols = ["ORDER NUMBER", "CONSIGNMENT", "MASS", "LENGTH", "WIDTH", "HEIGHT"]
    df2 = df2[cols].dropna(subset=["ORDER NUMBER"])

    items: List[Item] = []
    for _, row in df2.iterrows():
        items.append(
            Item(
                order=str(row["ORDER NUMBER"]),
                consignment=str(row["CONSIGNMENT"]),
                mass=float(row["MASS"]),
                length=float(row["LENGTH"]),
                width=float(row["WIDTH"]),
                height=float(row["HEIGHT"]),
                rotatable=True,
            )
        )
    return items


# ---------- example usage ----------

if __name__ == "__main__":
    # 1. read the 19 items from the workbook
    items = read_items_from_excel("19-GENSETS-VEHICLE-CONFIGURATION.xlsx")

    # 2. define trailer types.
    #    Replace deck_length / max_mass with your real trailer specs
    trailers = [
        TrailerType(name="Link1", deck_length=11.5, max_mass=18.0),
        TrailerType(name="Link2", deck_length=11.5, max_mass=18.0),
        TrailerType(name="Link3", deck_length=11.5, max_mass=18.0),
    ]

    loads = load_items_to_trailers(items, trailers, trailer_count=3, gap=0.0)

    # 3. print layout summary (you can turn this into a visual later)
    for load in loads:
        print(f"Trailer {load.index} ({load.trailer_type.name}) "
              f"- used length {load.used_length:.2f} m, mass {load.used_mass:.3f}")
        for p in load.placed_items:
            print(f"  {p.item.order} {p.item.consignment} "
                  f"{p.orientation} from {p.x_start:.2f} to {p.x_end:.2f}")
        print()
