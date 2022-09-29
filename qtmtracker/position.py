"""
3D positional tracking utilities.
"""

from typing import Iterable, Iterator, List, Sequence, Tuple

class PositionHistory:
    """
    Class to keep track of the last N positions of a marker

    Any new positions added to the history will overwrite the oldest position.
    """

    def __init__(self, size: int, id: int, label: str = "unlabelled marker"):
        """
        Create a new PositionHistory object

        :param size: The number of positions to keep track of
        :param id: The id of the marker
        :param label: The label of the marker
        """

        self.size: int = size
        self.id: int = id
        self.loc: int = 0
        self.filled: bool = False
        self.label: str = label
        self.empty: bool = True
        self.positions: List[Tuple[float, float, float]] = []

    def add(self, position: Tuple[float, float, float]):
        """
        Add a new position to the history

        :param position: The position to add
                         tuple of (x, y, z) coordinates
        """

        if not self.filled:
            item_count: int = len(self)
            if item_count < self.size:
                self.positions.append(position)
                self.empty = False
                self.loc = item_count
                if item_count == self.size - 1:
                    self.filled = True
            return

        self.loc = (self.loc + 1) % self.size
        self.positions[self.loc] = position

    def get(self, index: int) -> Tuple[float, float, float]:
        """ 
        Get a position from the history

        Forgiving of out of bounds indices, will wrap around.
        
        :param index: The index of the position to get
        """

        if self.empty:
            raise IndexError("PositionHistory is empty")

        index = (index) % self.size
        return self.positions[index]

    def last(self) -> Tuple[float, float, float]:
        """ Get the last position added to the history """

        if self.empty:
            raise IndexError("PositionHistory is empty")
        return self.get(self.loc)

    def first(self) -> Tuple[float, float, float]:
        """ Get the first _available_ position added to the history """

        if self.empty:
            raise IndexError("PositionHistory is empty")

        return self.get(self.loc + 1)

    def prev(self) -> Tuple[float, float, float]:
        """ Get the previous position added to the history """
        
        if self.empty:
            raise IndexError("PositionHistory is empty")
        
        return self.get(self.loc - 1)

    def velocity(self) -> Tuple[float, float, float]:
        """ Get the velocity of the marker """
        n_points: int = len(self)
        if n_points == 0:
            raise IndexError("PositionHistory is empty")
        elif n_points < 2:
            return (0.0, 0.0, 0.0)

        last: Tuple[float, float, float] = self.last()
        prev: Tuple[float, float, float] = self.prev()

        return (last[0] - prev[0], last[1] - prev[1], last[2] - prev[2])
    
    def distance(self) -> float:
        """ Get the distance travelled by the marker """

        n_points: int = len(self)
        if n_points == 0:
            raise IndexError("PositionHistory is empty")
        elif n_points < 2:
            return 0.0

        last: Tuple[float, float, float] = self.last()
        first: Tuple[float, float, float] = self.first()

        return ((last[0] - first[0]) ** 2 + (last[1] - first[1]) ** 2 + (last[2] - first[2]) ** 2) ** 0.5
    
    def __len__(self) -> int:
        """ Get the number of positions in the history """

        if self.empty:
            return 0

        if self.filled:
            return self.size

        return self.loc + 1
    
    def __iter__(self) -> Iterator[Tuple[float, float, float]]:
        """ Iterate over the positions in the history """

        if self.empty:
            return iter([])

        if self.filled:
            return iter(self.positions)

        return iter(self.positions[: self.loc + 1])
    
    def __getitem__(self, index: int) -> Tuple[float, float, float]:
        """ Get a position from the history """

        return self.get(index)
    
    def __str__(self) -> str:
        """ Get a string representation of the history """

        return f"PositionHistory({self.size}, {self.id}, {self.label})"
    
    def __repr__(self) -> str:
        """ Get a string representation of the history """

        return str(self)
        



class Markers:
    """
    Class to keep track of the positions of multiple markers
    """

    def __init__(self, marker_indices: Sequence[int], size: int, labels: Sequence[str] = []):
        """
        Create a new Markers object

        :param size: The size of the history of each marker
        """
        self.size: int = size
        self.markers: List[PositionHistory] = []
        self.index_map: dict = {}
        self.labels: Iterable[str] = labels
        for i, marker_idx in enumerate(marker_indices):
            try:
                self.add(marker_idx, labels[i])
            except IndexError:
                self.add(marker_idx)

    def add(self, marker_idx: int, label: str = ""):
        """
        Add a new marker to track.

        :param marker_idx: The index of the marker
        :param label: The label of the marker
        """
        if label == "":
            label = "unlabelled marker"
        self.index_map[marker_idx] = len(self.markers)
        self.markers.append(PositionHistory(self.size, marker_idx, label))

    def get(self, marker_idx: int) -> PositionHistory:
        """
        Get the position history of a marker

        :param marker_idx: The index of the marker
        """

        return self.markers[self.index_map[marker_idx]]
    
    def __len__(self) -> int:
        """ Get the number of markers being tracked """

        return len(self.markers)
    
    def __getitem__(self, idx: int) -> PositionHistory:
        """ Get the position history of a marker, by sequential index """

        return self.markers[idx]

    def __contains__(self, marker_idx: int) -> bool:
        """ Check if a marker is being tracked """

        return marker_idx in self.index_map

    def __str__(self) -> str:
        """ Get a string representation of the markers """

        return f"Markers({len(self)})"
    
    def __repr__(self) -> str:
        """ Get a string representation of the markers """

        return f"Markers({len(self)})"
    
    def __iter__(self) -> Iterator[PositionHistory]:
        """ Iterate over the markers """

        return self.markers.__iter__()