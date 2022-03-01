# Tips to work with supported networks

_In this document we will give hints about each network based on previous experience_

---



#### SSD resnet50

Like other SSD networks, this network aims to provide fast inference times.

- Default image size is 640*640.
  - It is always recommended to keep the batch size to a minimum with such image size.
- Training uses pretrained weights. 
  -  Takes more time to converge than mobilenet and inception. So training should be around 100 k steps.



#### Efficient Det D0 

This network aims to provide fast inference time with acceptable accuracy. 













​	

 