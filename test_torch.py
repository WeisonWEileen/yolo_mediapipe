import torch

a=torch.randn(1,2,3)
# print(a.shape)
# b=torch.squeeze(a)
# print(b.shape)
c=torch.squeeze(a,0)
print(c.shape)
# d=torch.squeeze(a,1)
# print(d.shape)
# e=torch.squeeze(a,2)#如果去掉第三维，则数不够放了，所以直接保留
# print(e.shape)