# Copyright 2024 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import timeit

import torch
from torch_int._CUDA import bmm_s8t_s8n_f32t


def mm(A, B):
    return torch._int_mm(A.squeeze(), B.squeeze().transpose(1, 0))


A = torch.randint(1, 10, [1, 512, 12288]).type(torch.int8).cuda()
B = torch.randint(1, 10, [1, 512, 12288]).type(torch.int8).cuda()
print(A)

# Using torch int matmul
# Warmup (slow)
mm(A, B)
# Average on several calls
it = 1000
print("torch _int_mm")
print(timeit.Timer(lambda: mm(A, B)).timeit(it) / it)

# Using torch_int custom kernels
# Warmup (slow)
bmm_s8t_s8n_f32t(A, B, 0.1)
# Average on several calls
it = 1000
print("torch_int kernels")
print(timeit.Timer(lambda: bmm_s8t_s8n_f32t(A, B, 0.1)).timeit(it) / it)

# Using torch f16 matmul
# Warmup (slow)
A = A.type(torch.float16)
B = B.type(torch.float16)
torch.matmul(A, B.transpose(2, 1))
# Average on several calls
it = 1000
print("torch fp16 matmul")
print(timeit.Timer(lambda: torch.matmul(A, B.transpose(2, 1))).timeit(it) / it)
