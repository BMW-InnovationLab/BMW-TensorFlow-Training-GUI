# Tips to work with supported networks

_In this document we will give hints about each network based on previous experience_

---

#### SSD MOBILENET

A network that focuses mainly on inference speed while still giving good accuracy results.

- Default image size is 300*300.
  - Increasing the image size (512 * 512 or 640 * 640) gives better accuracy results but you will have to decrease the batch size as it consumes more memory.
- Training uses pretrained weights. 
  - Training around 50k to 75k steps should be enough. Feel free to choose the number of steps you want as long as you have satisfying results



#### SSD INCEPTION

This network focuses also on inference speed but gives slightly better accuracy results than mobilenet. The outcome model is still relatively light.

Same hints that apply to mobilenet apply here because they have very similar config files.



#### SSD resnet50

Like other SSD networks, this network aims to provide fast inference times.

- Default image size is 640*640.
  - It is always recommended to keep the batch size to a minimum with such image size.
- Training uses pretrained weights. 
  -  Takes more time to converge than mobilenet and inception. So training should be around 100 k steps.



#### SSD resnet 50 FPN

This network is mainly the same as SSD resnet 50 but with feature pyramid support. Feature pyramid should help us detect small objects.

Same hints of SSD resnet 50, apply here.



#### FASTER RCNN models

Faster RCNN networks prioritize accuracy over inference speed. 

Both of the models offer good accuracy. 

- In these network the image size is not fixed. It varies between a min and max 
  - Images in these networks are too big. That's why the batch size should be very small (usually 1)
- Faster RCNN resnet 50 uses pretrained weights
  - Training steps around 75k to 100k
- Faster RCNN resnet 101 does not use pretrained weights
  - Training steps should be around 150k. 
  - Model takes time before it converges. 




## Benchmark Table

<html>

<table>

```
<thead align="center">
    <tr>
        <th></th>
        <th>Windows</th>
        <th colspan=3>Ubuntu</th>
    </tr>
</thead>
<thead align="center">
    <tr>
        <th>Network\Hardware</th>
        <th>Intel Xeon CPU 2.3 GHz</th>
        <th>Intel Xeon CPU 2.3 GHz</th>
        <th>Intel Xeon CPU 3.60 GHz</th>
        <th>GeForce GTX 1080</th>
    </tr>
</thead>
<tbody align="center">
    <tr>
        <td>ssd_fpn</td>
        <td>0.867 seconds/image</td>
        <td>1.016 seconds/image</td>
        <td>0.434 seconds/image</td>
        <td>0.0658 seconds/image</td>
    </tr>
    <tr>
        <td>frcnn_resnet_50</td>
        <td>4.029 seconds/image</td>
        <td>4.219 seconds/image</td>
        <td>1.994 seconds/image</td>
        <td>0.148 seconds/image</td>
    </tr>
    <tr>
        <td>ssd_mobilenet</td>
        <td>0.055 seconds/image</td>
        <td>0.106 seconds/image</td>
        <td>0.051 seconds/image</td>
        <td>0.052 seconds/image</td>
    </tr>
    <tr>
        <td>frcnn_resnet_101</td>
        <td>4.469 seconds/image</td>
        <td>4.985 seconds/image</td>
        <td>2.254 seconds/image</td>
        <td>0.364 seconds/image</td>
    </tr>
    <tr>
        <td>ssd_resnet_50</td>
        <td>1.34 seconds/image</td>
        <td>1.462 seconds/image</td>
        <td>0.668 seconds/image</td>
        <td>0.091 seconds/image</td>
    </tr>
    <tr>
        <td>ssd_inception</td>
        <td>0.094 seconds/image</td>
        <td>0.15 seconds/image</td>
        <td>0.074 seconds/image</td>
        <td>0.0513 seconds/image</td>
    </tr>
</tbody>
```

</table>

</html>











​	

 