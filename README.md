# QTM Python 3D Tracking

A python module that allows for easily gathering 3D tracking data from Qualisys Track Manager (QTM) using the QTM SDK.

## Installation

Clone this repository, then run `pip install .` in the root directory.

### Prerequisites

- Python 3.8+

## Usage

The first steps are to create a config object, which defines the markers you want to track as well as the QTM server, and how many position history locations you want to store for each 3D marker.

```python
import qtmtracker
qtm_config = qtmtracker.QTMConfig(SERVER_IP, QTM_MARKER_INDICES, LENGTH_OF_POSITION_HISTORY, OPTIONAL_LABELS)
```
    
Then, create a tracker object, which will prepare the markers, history and QTM connection.
    
```python
# this initializes the tracker object with the config you just specified
qtm_tracker = qtmtracker.QTMTracker(qtm_config)

```

To make this useful, you'll need to have a defined callback function that will execute every time a frame is recieved from QTM. This function should return a boolean which means whether or not to continue tracking. If you want to stop tracking, return False. If you want to continue tracking, return True.

```python
def cool_callback_function(tracker):
    # do something with the tracker object
    return True

# add this callback function to the tracker
qtm_tracker.set_frame_callback(cool_callback_function)

```

Then, start the tracker, which will run indefinitely until the callback function returns False.

```python
# start the tracking loop
qtm_tracker.run()

```

### Markers

Markers are retrieved via the tracker object that is passed into the callback function. Markers give you access to the position history of each tracked marker.

Markers can be iterated over, as well as accessed by their sequential index or QTM index/id.

```python
# get the markers from the tracker
markers = tracker.markers

# iterate over the markers
for marker in markers:
    # do something with the marker

# get a marker by sequential index
marker = markers[0]

# get a marker by QTM index
marker = markers.get(7)

```

Retrieved markers give you a `PositionHistory` object which provides some convienience methods for accessing the position history of the marker.

```python

# get the current position of the marker
# returns a tuple of (x, y, z)
position = marker.last()

# get the first available position of the marker from the history
position = marker.first()

# get the previous position of the marker, if your  history size is 2, this is the same as calling marker.first()
position = marker.prev()

# there are also currently two methods for calculatining movement

# get the distance between the current position and the previous position
# returns a float with the absolute difference travelled
distance = marker.distance()

# get the velocity vector between the current position and the previous position
# returns a tuple of (x, y, z)
velocity = marker.velocity()

```


### Usage Example


Complete example of tracking a 2 3D markers, printing out their positions for 100 frames as well as some summary data.


```python
# https://github.com/zeyus/qtmtracker/blob/main/qtm_read_example.py

import qtmtracker

# QTM server IP address
QTM_SERVER: str = "127.0.0.1"

# List of markers to track.
MARKER_INDICES: tuple = (
    7,
    9,
)

# Labels are just for reference
# they are optional, as right now, there
# is no way to get the marker names from QTM
# but I will invistigate a workaround,
# as label matching is easier than index matching
# for users.
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

    # Now print the current position of a specific marker.
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

```