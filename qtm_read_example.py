"""
  Qualisys Track Manager (QTM) read example.

  Requires python 3.8 or later.
  Dependencies: qtmtracker

  https://github.com/zeyus/qtmtracker

  See also: https://qualisys.github.io/qualisys_python_sdk/index.html
"""

import qtmtracker



# QTM server IP address
QTM_SERVER: str = "127.0.0.1"

# List of markers to track.
MARKER_INDICES: tuple = (
    7,
    9,
)

MARKER_LABELS: tuple = (
    "Marker A Name",	
    "Marker B Name",
)

# how many previous positions to keep
POSITION_HISTORY_LENGTH: int = 2

# if this function returns False then the loop stops
def print_example_info(tracker: qtmtracker.QTMTracker) -> bool:
    # Print the distance travelled by each marker.
    for marker_history in tracker.markers:
        print(f"{marker_history}: {marker_history.distance():.3f}")


    # this is to get the first added marker
    marker_history: qtmtracker.PositionHistory = tracker.markers[0]

    # or we can get a marker by it's QTM index
    marker_history_2: qtmtracker.PositionHistory = tracker.markers.get(MARKER_INDICES[1])

    # Now rint the current position of a specific marker.
    print(f"{marker_history_2} current coordinates: {marker_history_2.last()}")
    # or
    x, y, z = marker_history_2.last()
    print(f"{marker_history_2} coordinates: {x:.3f}, {y:.3f}, {z:.3f}")

    # Now let's get the velocity of maker A
    print(f"{marker_history} velocity: {marker_history.velocity()}")

    # now we can exit if we've processed over 100 frames
    if tracker.frame_count > 100:
        print("Processed 100 frames, exiting")
        return False
    
    return True



if __name__ == "__main__":
    qtm_config = qtmtracker.QTMConfig(QTM_SERVER, MARKER_INDICES, POSITION_HISTORY_LENGTH, MARKER_LABELS)
    qtm_tracker = qtmtracker.QTMTracker(qtm_config)
    qtm_tracker.set_frame_callback(print_example_info)
    qtm_tracker.run()
