import numpy as np
import json


class Position:
    """The wrapper class for position of object
    """

    def __init__(self, clz=None, phi=None, coordinate: np.ndarray = None, obj: dict = None) -> None:
        """The constructor of Position

        Args:
            clz (class, optional): The class of this object. Defaults to None.
            phi (angle, optional): The angle of object. Defaults to None.
            coordinate ([x, y], optional): Base x-axis and y-axis. Defaults to None.
            obj (needed to be serialization, optional): the object to be deserialization. Defaults to None.
        """
        if obj:
            self.clz = obj["clz"]
            self.phi = obj["phi"]
            self.coordinate = np.array(obj["coordinate"])
        else:
            self.clz = clz
            self.phi = phi
            self.coordinate = coordinate

    def serialization(self) -> dict:
        """serialization
        Returns:
            json: the obj of position
        """
        return {
            "clz": self.clz,
            "phi": self.phi,
            "coordinate": self.coordinate.tolist()
        }


class __PositionBase:
    """The test class for serialization
    """

    def __init__(self, clz, phi, coordinate: np.ndarray) -> None:
        self.clz = clz
        self.phi = phi
        self.coordinate = coordinate


if __name__ == "__main__":
    p = Position(1, 15, np.array([1, 2, 3]))
    print(f"p: {p.serialization()}")
    pp = Position(obj=p.serialization())
    print(f"pp: {pp.serialization()}")
