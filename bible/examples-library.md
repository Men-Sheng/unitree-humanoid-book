# bible/examples-library.md — 范例库

> Writer 起草时从这里取"已经跑通过的东西"的结构，不重新发明。
> 每条：来源 + 版本 + 它示范什么 + 是否可复制（license）。

| # | 来源 | 版本/commit | 示范什么 | 可复制性 |
|---|---|---|---|---|
| 1 | `unitree_sdk2_python/example/helloworld/{publisher,subscriber}.py` | master 2026-10 抓取 | 最小收发骨架、`ChannelFactoryInitialize(id, nic)` 用法 | BSD-3，可改可复制并注明 |
| 2 | `example/a2/sport/a2_sport_state.py` | 同上 | 带 handler + 队列的订阅写法、`mode` 状态名表 | 同上 |
| 3 | `example/go2/high_level/go2_sport_client.py` | 同上 | 高层动作调用与选项 id 表 | 同上 |
| 4 | `example/go2/low_level/go2_stand_example.py` | 同上 | 低层起立的时序与限幅处理 | 同上，但需 EDU |
| 5 | `example/go2/front_camera/camera_opencv.py` | 同上 | WebRTC 图传取帧 | 同上 |
| 6 | `example/motion_switcher/motion_switcher_example.py` | 同上 | 控制权抢占与能力查询 | 同上 |
| 7 | `unitree_mujoco` 的 Go2 配置 | MuJoCo 3.3.6 | 仿真侧同话题复现 | BSD-3 |
| 8 | `unitree_rl_lab` 的 `-l/-t` 脚本 | 2026-05 | 训练入口与 USD 资产获取 | Apache-2.0 |
| 9 | `go2_ros2_sdk`（社区） | 1048★ | 固件断代事实的记录方式 | BSD-2 |

**规则**：范例只借结构与接口形状，正文代码一律自己重写并跑通；不可复制的（无 LICENSE / CC BY-NC-SA / GPL）只描述行为。
