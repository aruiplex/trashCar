# trashCar


The config.json file specification

```json5
{
  "cv": {
    // weight file location .pt file
    "weights": "./sense/trash.pt",
    /*
    alinux develop env rgb camera number: 4,
    Jetson nano product env rgb camera number: 2,
     */
    "rgb_source": 4,
    // image size, here we use 640*480
    "imgsz": 640,
    // confidence threshold
    "conf_thres": 0.6,
    "iou_thres": 0.45
  },
  "data_filter": {
    /*
    data filter range, [n * -sigma, n * sigma]
    */  
    "std_range": 3,
    /*
    The x sampling method for obj depth detection,
    Here are the unit points 
    */
    "sampling_method_x": [
      [0.125, 0.125],
      [0.25, 0.25],
      [0.375, 0.375],
      [0.5, 0.5],
      [0.625, 0.625],
      [0.75, 0.75],
      [0.875, 0.875],
      [0.125, 0.875],
      [0.25, 0.75],
      [0.375, 0.625],
      [0.625, 0.375],
      [0.75, 0.25],
      [0.875, 0.125]
    ]
  },
  "car_framework": {
    "camera_bias_arm": 0,
    "rgb_camera": {
      "x_pixels": 640,
      "y_pixels": 480
    }
  }
}
```
