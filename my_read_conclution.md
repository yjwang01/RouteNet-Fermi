# datasets_format

## traffic.txt



traffic_intensity(maxAvgLambda) | `FLOWS`

`FLOWS`:

每一个`FLOW`以`;` 间隔

TimeDist(流量模型，泊松等) + 根据流量模型的定义的不同长度的参数

SizeDist(数据包大小分布) + 参数

ToS（最后一个元素）是什么意思？

![image-20250108165323312](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108165323363.png)

一共的`FLOW`数量为 节点数*节点数

以src, dst排布

## simulationResults.txt

在`|`前分别是

   ```
   s._set_global_packets(first_params[0])
   s._set_global_losses(first_params[1])
   s._set_global_delay(first_params[2])
   ```

在`|`后分别是

```
q_flows.put([tmp_result_flow[0], tmp_result_flow[1]])
dict_result_tmp = {'PktsDrop':tmp_result_flow[2], "AvgDelay":tmp_result_flow[3], "AvgLnDelay":tmp_result_flow[4], "p10":tmp_result_flow[5], "p20":tmp_result_flow[6], "p50":tmp_result_flow[7], "p80":tmp_result_flow[8], "p90":tmp_result_flow[9], "Jitter":tmp_result_flow[10]}
```

![image-20241222000349510](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/202412220003625.png)

> AvgBW：kbps
>
> PktsGen：packets per second



超图中具有很多节点，包括`FLOWS，QUEUES，LINKS`

超图中的边是指具有关系的边，例如FLOWS和它经过的LINKS有关，

## linkUsage.txt

一共的`FLOW`数量为 节点数*节点数

以src, dst排布

表示每一条链路的利用率

如果该链路未使用，则记为 -1；

否则：

前三个数值分别表示该条链路的 `utilization`，`losses`，`avgPacketSize` 情况；

后面参数以五个为一组，表示一个队列优先级相关的信息，分别为：

`utilization`, `losses`,`avgPortOccupancy`,`maxQueueOccupancy`,`avgPacketSize`

```python
for i in range(netSize):
    port_stat.append({})
    for j in range(netSize):
        params = l[i*netSize+j].split(",")
        if (params[0] == "-1"):
            continue
        link_stat = {}
        link_stat["utilization"] = float(params[0])
        link_stat["losses"] = float(params[1])
        link_stat["avgPacketSize"] = float(params[2])
        num_qos_queues = int((len(params)-3)/5)
        qos_queue_stat_lst = []
        for q in range(num_qos_queues):
            qos_queue_stat = {"utilization":float(params[3+q*5]),
                          "losses":float(params[3+q*5+1]),
                          "avgPortOccupancy":float(params[3+q*5+2]),
                          "maxQueueOccupancy":float(params[3+q*5+3]),
                          "avgPacketSize":float(params[3+q*5+4])}
            qos_queue_stat_lst.append(qos_queue_stat)
        link_stat["qosQueuesStats"] = qos_queue_stat_lst;
        port_stat[i][j] = link_stat
```

![image-20241222002650180](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/202412220026217.png)

![image-20241222003054313](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/202412220030350.png)

# DatanetAPI





# Sample

  global_packets = None

  global_losses = None

  global_delay = None

  maxAvgLambda = None



---



## `routing_matrix`

src-dest的矩阵，元素内容为 path



---

## `topology_object`（g）

拓扑关系图



---

## `port_stats`

src-dest

`port_stats` 是一个列表，包含 `NODES_NUM` 个 dict

每个dict的key是dest，内容为 `link_stat`

### `link_stat`

每个链路的状态

{"utilization"， "losses"， "avgPacketSize",  ”qosQueuesStats“ }

qosQueuesStats 是一个 list，每个元素包含以下内容：

{"utilization", "losses", "avgPortOccupancy", "maxQueueOccupancy", "avgPacketSize"}

相当于每一个 src 到 dest 的链路，分优先级队列进行统计的。



---

## `performance_matrix`（m_result）：

包含 `n * n` 个`dict_result_srcdst`

![image-20250107221509333](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250107221516488.png)

### `dict_result_srcdst`

{"'AggInfo'"：`dict_result_agg`，”Flows”：`lst_result_flows`}

一个是总的，一个是分流的，但是具有相同的`src`和`dest`

#### `dict_result_agg`

{"PktsDrop", "AvgDelay", "AvgLnDelay", "p10", "p20", "p50", "p80", "p90", "Jitter"}

#### `lst_result_flows`

{"PktsDrop", "AvgDelay", "AvgLnDelay", "p10", "p20", "p50", "p80", "p90", "Jitter"}，共有FLOWS个



---

## `traffic_matrix`（m_traffic）：

包含 `n * n` 个`dict_traffic_srcdst`

### `dict_traffic_srcdst`

{"'AggInfo'"：`dict_traffic_agg`，”Flows”：`lst_traffic_flows`}

#### `dict_traffic_agg`

{"AvgBw", "PktsGen", "TotalPktsGen"}

#### `lst_traffic_flows`

{"TimeDist", "TimeDistParams", "SizeDist", "SizeDistParams", "AvgBw", "PktsGen", "TotalPktsGen", "ToS"}，共有FLOWS个



# HyperGraph

## Nodes

- `l_{src}_{dst}`  Links

  - capacity

    src到dst的带宽

  - policy

    链路策略的枚举值，FIFO，多优先级等的调度策略

- `p_{src}_{dst}_{f_id}`  Paths，Performances，Flows

  - source

  - destination
  - tos
  - traffic

  从 src 到 dst 的 AvgBW

  - packets

  这条流上一共产生的包的个数

  - delay

  链路上的平均时延

  - length

  从 src 到 dst 的路径的长度，links的数量，相当于 len(sn_path) - 1

  - model

  业务中的分布模型 TimeDist

  - eq_lambda
  - avg_pkts_lambda
  - exp_max_factor
  - pkts_lambda_on
  - avg_t_off
  - avg_t_on
  - ar_a
  - sigma

  针对不同的TimeDist所具有的参数集，没有就是0

- `q_{h_1}_{h_2}_{queue_id}`

  ![image-20250107230504949](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250107230505024.png)

  - queue_size

  为什么是这样子计算啊，对于不同的队列有不同的数值

  ![image-20250107230605453](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250107230605487.png)

  - priority

  这个队列的优先级

  - weight

  不知道什么东西




- `queue_to_path` 和 `link_to_path` 的数量相同

`T[src, dst]['Flows'][0]['ToS']` 表明了这个 `Flow` 的

```python
for q in range(G.nodes[h_1]['levelsQoS']):
    D_G.add_node('q_{}_{}_{}'.format(h_1, h_2, q),
                 queue_size=int(q_s[q]),
                 priority=q_n,
                 weight=q_w[q] if q_w[0] != '-' else 0)

    D_G.add_edge('q_{}_{}_{}'.format(h_1, h_2, q), 'l_{}_{}'.format(h_1, h_2))
    if str(int(T[src, dst]['Flows'][0]['ToS'])) in q_map[q]:
        D_G.add_edge('p_{}_{}_{}'.format(src, dst, f_id), 'q_{}_{}_{}'.format(h_1, h_2, q))
        D_G.add_edge('q_{}_{}_{}'.format(h_1, h_2, q), 'p_{}_{}_{}'.format(src, dst, f_id))
    q_n += 1
```







# Input data

```python 
return {
    # shape (182, 1), 不是为了适配multigraph，一个src-dest有多个flows，因为不同的flow已经有对应的fd_id的编号（单独一个节点）了
    "traffic": np.expand_dims(list(nx.get_node_attributes(HG, 'traffic').values()), axis=1),
    "packets": np.expand_dims(list(nx.get_node_attributes(HG, 'packets').values()), axis=1),
	# list 182
    "length": list(nx.get_node_attributes(HG, 'length').values()),
    # list 182 全是 [1]
    "model": list(nx.get_node_attributes(HG, 'model').values()),
	# shape (182, 1)
    "eq_lambda": np.expand_dims(list(nx.get_node_attributes(HG, 'eq_lambda').values()), axis=1),
    "avg_pkts_lambda": np.expand_dims(list(nx.get_node_attributes(HG, 'avg_pkts_lambda').values()), axis=1),
   	# shape (182, 1) 全是[0]
    "exp_max_factor": np.expand_dims(list(nx.get_node_attributes(HG, 'exp_max_factor').values()), axis=1),
    "pkts_lambda_on": np.expand_dims(list(nx.get_node_attributes(HG, 'pkts_lambda_on').values()), axis=1),
    "avg_t_off": np.expand_dims(list(nx.get_node_attributes(HG, 'avg_t_off').values()), axis=1),
    "avg_t_on": np.expand_dims(list(nx.get_node_attributes(HG, 'avg_t_on').values()), axis=1),
    "ar_a": np.expand_dims(list(nx.get_node_attributes(HG, 'ar_a').values()), axis=1),
    "sigma": np.expand_dims(list(nx.get_node_attributes(HG, 'sigma').values()), axis=1),
    # shape (42, 1) 
    "capacity": np.expand_dims(list(nx.get_node_attributes(HG, 'capacity').values()), axis=1),
    "queue_size": np.expand_dims(list(nx.get_node_attributes(HG, 'queue_size').values()), axis=1),
    # list 42 全是[3]，对应‘FIFO’
    "policy": list(nx.get_node_attributes(HG, 'policy').values()),
    # list 42 全是[0]，只有一个队列现在
    "priority": list(nx.get_node_attributes(HG, 'priority').values()),
    # shape (42, 1) 全是[0]
    "weight": np.expand_dims(list(nx.get_node_attributes(HG, 'weight').values()), axis=1),
    # list 182，元素为变长列表
    "link_to_path": tf.ragged.constant(link_to_path),
    "queue_to_path": tf.ragged.constant(queue_to_path),
    # list 42， 元素为定长列表？长度为1
    "queue_to_link": tf.ragged.constant(queue_to_link),
    "path_to_queue": tf.ragged.constant(path_to_queue, ragged_rank=1),
    "path_to_link": tf.ragged.constant(path_to_link, ragged_rank=1)}, 

	list(nx.get_node_attributes(HG, 'delay').values())
```



queue_to_link 表示消息传递方向，queue的消息需要传递给link

queue_gather = tf.gather(queue_state, queue_to_link) 用来获取本link需要哪些queue的消息，聚集了一些信息

再通过RNN link_update网络来

![image-20250108135102135](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108135102225.png)

![image-20250108135112898](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108135112939.png)

![image-20250108135203022](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108135203070.png)

![image-20250108135233637](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108135233690.png)

![image-20250108135302283](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108135302336.png)

![image-20250108135641737](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108135641808.png)

# **Call**

### `traffic`

`TensorShape([182, 1])`

![image-20250108152518674](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108152518714.png)

![](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108152430810.png)

### `packets`

`TensorShape([182, 1])`

![image-20250108152725684](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108152725718.png)

![image-20250108152627708](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108152627758.png)

### `length`

`TensorShape([182])`

表示每个path的长度，以`link`计

![image-20250108152828028](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108152828072.png)

### `capacity`

`TensorShape([42, 1])`

![image-20250111143326088](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250111143326254.png)

![image-20250111143334444](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250111143334484.png)

### `policy`

`TensorShape([42, 4])`

![image-20250108152905084](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108152905117.png)

![image-20250108152919316](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108152919355.png)

### `priority`

`TensorShape([42, 3])`

![image-20250108153036291](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108153036337.png)

![image-20250108153044579](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108153044618.png)

### `queue_to_path`

`TensorShape([182, 1])` 但是是变长元素，`tf.RaggedTensor`

![image-20250108153915429](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108153915473.png)

### `link_to_path`

`TensorShape([182, 1])`,` tf.RaggedTensor`

![image-20250108154104701](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108154104745.png)

### `path_to_link`

`TensorShape([42, None, 2])`

![image-20250108154250286](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108154250335.png)

![image-20250108154310861](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108154310905.png)

### `path_to_queue`

`TensorShape([42, None, 2])`

一共有42个queue（link），每个queue可能属于很多个path，path的长度即 `path_to_queue[i]` 的长度，

每一个 `path_to_queue[i][j]` 对应一个二元组，表示这个 queue （和哪个path有关，属于path路径中的第几个）

第几个在计算 `path_gather`的时候起到作用，

![image-20250108154449104](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108154449158.png)

### `queue_to_link`

`TensorShape([42, 1])`

![image-20250108154833876](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108154833923.png)

![image-20250108154840068](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108154840097.png)

### `path_gather_traffic`

`TensorShape([42, None, 1])`

```path_gather_traffic = tf.gather(traffic, path_to_link[:, :, 0])```

![image-20250108211015469](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108211017164.png)

以 `path_to_link[ : , : ,0]` 作为索引，以 填入 `traffic` 中的值

最终`path_gather_traffic[i]`中包含了经过 第`i`条 `link` 的所有 `path` 的流量需求。

![image-20250108162739111](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250108162739167.png)

### `load`

`TensorShape([42, 1])`

```load = tf.math.reduce_sum(path_gather_traffic, axis=1) / capacity```

表示每一个链路的负载强度 [0，1]

### `pkt_size`

`TensorShape([182, 1])` bits

### `path_state`

`TensorShape([182, 32])`

`path_feature` （`TensorShape([182, 17])`）经过 `path_embedding `网络后得到嵌入结果 `path_state`。

```python
path_feature = tf.concat(
            [(traffic - self.z_score['traffic'][0]) / self.z_score['traffic'][1],
             (packets - self.z_score['packets'][0]) / self.z_score['packets'][1],
             tf.one_hot(model, self.max_num_models),
             (eq_lambda - self.z_score['eq_lambda'][0]) / self.z_score['eq_lambda'][1],
             (avg_pkts_lambda - self.z_score['avg_pkts_lambda'][0]) / self.z_score['avg_pkts_lambda'][1],
             (exp_max_factor - self.z_score['exp_max_factor'][0]) / self.z_score['exp_max_factor'][1],
             (pkts_lambda_on - self.z_score['pkts_lambda_on'][0]) / self.z_score['pkts_lambda_on'][1],
             (avg_t_off - self.z_score['avg_t_off'][0]) / self.z_score['avg_t_off'][1],
             (avg_t_on - self.z_score['avg_t_on'][0]) / self.z_score['avg_t_on'][1],
             (ar_a - self.z_score['ar_a'][0]) / self.z_score['ar_a'][1],
             (sigma - self.z_score['sigma'][0]) / self.z_score['sigma'][1]], axis=1)
```

### `link_state`

`TensorShape([42, 32])`

`link_feature` （`TensorShape([42, 5])`）经过 `link_embedding `网络后得到嵌入结果 `link_state`。

```python
link_feature = tf.concat([load, policy], axis=1)
```



### `queue_state`

`TensorShape([42, 32])`

`queue_feature` （`TensorShape([42, 5])`）经过 `queue_embedding `网络后得到嵌入结果 `queue_state`。

```python
queue_feature = tf.concat([(queue_size - self.z_score['queue_size'][0]) / self.z_score['queue_size'][1],
                       priority, weight], axis=1)
```



### `queue_gather`

`TensorShape([182, 1, 32])` 但是是变长元素，`tf.RaggedTensor`

queue_gather[x].shape 可能是不同的

![image-20250109202018744](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250109202018784.png)

![image-20250109201831830](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250109201832216.png)

![image-20250109201850661](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250109201850708.png)

### `link_gather`

`TensorShape([182, 1, 32])` 但是是变长元素，`tf.RaggedTensor`

![image-20250110121756429](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250110121756477.png)

### `path_state_sequence`

`TensorShape([182, None, 32])`

每一个path由不同长度的link组成，因此每一个path的索引 `path_state_sequence[i]` 的形状是 `(None, 32)`

每一个 link 具有不同的状态信息，即 `path_state_sequence[i][j]`，维度为 32



由 `tf.concat([queue_gather, link_gather], axis=2)` （`TensorShape([182, None, 64])`）经过 RNN 后得到的每一个时间步的结果，

> [史上最详细循环神经网络讲解（RNN/LSTM/GRU） - 知乎](https://zhuanlan.zhihu.com/p/123211148)

> [path_update_rnn](vscode-file://vscode-app/c:/Program Files/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)是一个由 [tf.keras.layers.RNN](vscode-file://vscode-app/c:/Program Files/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) 包装的循环神经网络（RNN），它使用了 [GRUCell](vscode-file://vscode-app/c:/Program Files/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) 作为其基本单元。[GRUCell](vscode-file://vscode-app/c:/Program Files/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) 是一种门控循环单元（Gated Recurrent Unit），用于处理序列数据。
>
> ### 详细解释
>
> 1. **定义 [GRUCell](vscode-file://vscode-app/c:/Program Files/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)**：
>
>    self.path_update = tf.keras.layers.GRUCell(self.path_state_dim)
>
>    这里定义了一个 GRU 单元，[self.path_state_dim](vscode-file://vscode-app/c:/Program Files/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) 是 GRU 单元的输出维度。
>
> 2. **定义 [RNN](vscode-file://vscode-app/c:/Program Files/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) 层**：
>
>    path_update_rnn = tf.keras.layers.RNN(self.path_update,
>
>    ​                   return_sequences=True,
>
>    ​                   return_state=True)
>
>    这里定义了一个 RNN 层，使用前面定义的 [GRUCell](vscode-file://vscode-app/c:/Program Files/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) 作为其基本单元。[return_sequences=True](vscode-file://vscode-app/c:/Program Files/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) 表示返回每个时间步的输出，[return_state=True](vscode-file://vscode-app/c:/Program Files/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) 表示返回最后一个时间步的状态。
>
> ### 输入数据
>
> 假设输入数据的形状为 `TensorShape([182, None, 64])`，其中：
>
> - `182` 是批次大小（batch size）。
> - `None` 是时间步数（time steps），表示序列的长度可以变化。
> - `64` 是每个时间步的特征维度（feature dimension）。
>
> ### 处理过程
>
> 当输入数据通过 [path_update_rnn](vscode-file://vscode-app/c:/Program Files/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) 时，RNN 层会逐时间步处理输入数据，并返回每个时间步的输出和最后一个时间步的状态。

在经过 `path_state_sequence = tf.concat([tf.expand_dims(previous_path_state, 1), path_state_sequence], axis=1)`后的打印结果：

每一个 `path_state_sequence[i]` 的长度相比 `queue_to_path[i]` 的长度多了一个.

<font color=red> 为什么要这样把初始path_state放到最前面</font>

![image-20250110133705935](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250110133706043.png)

### `path_gather`

`TensorShape([42, None, 32])`

`path_gather = tf.gather_nd(path_state_sequence, path_to_queue)`

tf.gather_nd 用于从张量中提取多维索引指定的元素。与 [tf.gather](vscode-file://vscode-app/c:/Program Files/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) 不同，[tf.gather_nd](vscode-file://vscode-app/c:/Program Files/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) 可以处理多维索引，从而允许更灵活的元素提取。

此处

 `path_to_queue.shape = TensorShape([42, None, 2])`

`path_state_sequence.shape = TensorShape([182, None, 32])`

以 `path_to_queue[i][j]`的二元组 `(x,y)`作为 `path_state_sequence`的索引，得到 `path_state_sequence[x][y]` 作为 `path_to_queue` 的元素值，因此最终得到的 `path_gather.shape = TensorShape([42, None, 32]) `。（二元组使用索引到的 32维向量替代）

### `path_sum`

`TensorShape([42, 32])`

`path_sum = tf.math.reduce_sum(path_gather, axis=1)`

将 `path_gather` （`TensorShape([42, None, 32])`）沿着第一维度求和，得到这个 `path` 中所有链路组合成的状态

### `queue_gather`

`TensorShape([42, 1, 32])`

`queue_gather = tf.gather(queue_state, queue_to_link)`

### `capacity_gather`

`TensorShape([182, 1, 1])` ` tf.RaggedTensor`

`capacity_gather = tf.gather(capacity, link_to_path)` 

![image-20250111145637928](https://raw.githubusercontent.com/yjwang01/img_bed/main/img/20250111145637980.png)

### `input_tensor`

`TensorShape([182, 3, 32])`

`input_tensor = path_state_sequence[:, 1:].to_tensor()` 将稀疏张量转换为密集张量

### `occupancy_gather`

`TensorShape([182, 3, 1])`

`input_tensor` 经过全连接网络输出后，独立的得到不同时间步的结果，182为batch_size,3为时间步，32为输入特征维度，1为输出特征维度

`occupancy_gather = tf.RaggedTensor.from_tensor(occupancy_gather, lengths=length)`

将密集张量根据每个path的长度转化为稀疏张量

### `queue_delay`

`queue_delay = tf.math.reduce_sum(occupancy_gather / capacity_gather, axis=1)`

将路径上的所有队列delay求和

### `trans_delay`

根据这个队列的数据包长度得到传输时延



# Conclusion

每一次的仿真结果相当于一组batch

batch size 为仿真中的有效链路数量



