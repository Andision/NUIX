import React from 'react';
import axios from 'axios';
import {
  AndroidOutlined,
  AppleOutlined,
  WindowsOutlined,
  DeleteOutlined,
  EditOutlined,
  EllipsisOutlined,
  ReloadOutlined,
} from '@ant-design/icons';
import { Tabs, Card, List, Button, PageHeader } from 'antd';
import './AirClip.css';

const { TabPane } = Tabs;

const data1 = [
  {
    content: '这里是剪贴板',
    time: '2022-08-08 08:08:08',
  },
  {
    content: '一些复制的内容的样例',
    time: '2022-08-08 08:08:08',
  },
  {
    content: '卡片下部分是复制的内容',
    time: '2022-08-08 08:08:08',
  },
  {
    content: '卡片上部分是时间',
    time: '2022-08-08 08:08:08',
  },
  {
    content:
      '这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本',
    time: '2022-08-08 08:08:08',
  },
  {
    content:
      '这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本',
    time: '2022-08-08 08:08:08',
  },
  {
    content:
      '这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本',
    time: '2022-08-08 08:08:08',
  },
  {
    content:
      '这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本',
    time: '2022-08-08 08:08:08',
  },
];
const data2 = [
  {
    content: '还可以切换其他设备',
    time: '2022-08-08 08:08:08',
  },
  {
    content: '查看多个设备的剪贴板内容',
    time: '2022-08-08 08:08:08',
  },
  {
    content: '所有设备通过标签的方式显示在上方👆',
    time: '2022-08-08 08:08:08',
  },
  {
    content: '这里是剪贴板',
    time: '2022-08-08 08:08:08',
  },
  {
    content: '一些复制的内容的样例',
    time: '2022-08-08 08:08:08',
  },
  {
    content: '卡片下部分是复制的内容',
    time: '2022-08-08 08:08:08',
  },
  {
    content: '卡片上部分是时间',
    time: '2022-08-08 08:08:08',
  },
  {
    content:
      '这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本',
    time: '2022-08-08 08:08:08',
  },
  {
    content:
      '这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本',
    time: '2022-08-08 08:08:08',
  },
  {
    content:
      '这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本',
    time: '2022-08-08 08:08:08',
  },
  {
    content:
      '这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本这是长文本',
    time: '2022-08-08 08:08:08',
  },
  {
    content:
      '这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n这是换行\n',
    time: '2022-08-08 08:08:08',
  },
];

class AirClip extends React.Component {
  URL_PREFIX = 'http://localhost:5000/app/airclip';

  constructor(props) {
    super(props);

    this.getClipboard();

    // this.getClipboard = this.getClipboard.bind(this)

    this.state = {
      v: 100,
      realData: [],
      //   realData: [
      //     {
      //       content: '剪贴板',
      //       time: '2022-08-08 08:08:08',
      //     },
      //     {
      //       content: '样例',
      //       time: '2022-08-08 08:08:08',
      //     }
      //   ],
    };
  }

  getClipboard = () => {
    console.log('click refresh!');
    axios.get(`${this.URL_PREFIX}/get_clip`).then((response) => {
      // console.log(response);
      // return response.data;
      const ret = response.data;
      console.log('ret', ret);
      this.setState({ realData: ret });
      return ret;
    });
  };

  cutStr = (str, L) => {
    let result = '';
    const strlen = str.length; // 字符串长度
    const chrlen = str.replace(/[^\x00-\xff]/g, '**').length; // 字节长度

    if (chrlen <= L) {
      return str;
    }

    for (let i = 0, j = 0; i < strlen; i++) {
      const chr = str.charAt(i);
      if (/[\x00-\xff]/.test(chr)) {
        j++; // ascii码为0-255，一个字符就是一个字节的长度
      } else {
        j += 2; // ascii码为0-255以外，一个字符就是两个字节的长度
      }
      if (j <= L) {
        // 当加上当前字符以后，如果总字节长度小于等于L，则将当前字符真实的+在result后
        result += chr;
      } else {
        // 反之则说明result已经是不拆分字符的情况下最接近L的值了，直接返回
        if (result == str) {
          return result;
        }

        return `${result} ......`;
      }
    }
  };

  render() {
    return (
      <div className="my-app">
        <PageHeader
          className="page-header"
          onBack={() => (window.location.href = '/')}
          title="AirClip"
          subTitle=""
        />
        <Tabs
          defaultActiveKey="0"
          tabBarExtraContent={
            <Button
              onClick={() => {
                this.getClipboard();
              }}
            >
              <ReloadOutlined />
            </Button>
          }
        >
          <TabPane
            tab={
              <span>
                <WindowsOutlined />
                Andision's ThinkPad X1C （本机）
              </span>
            }
            key="0"
          >
            <List
              grid={{ gutter: 16, column: 1 }}
              dataSource={data1}
              renderItem={(item) => (
                <List.Item>
                  <Card
                    size="small"
                    title={item.time}
                    // actions={[
                    //   <DeleteOutlined key="setting" />,
                    //   <EditOutlined key="edit" />,
                    //   <EllipsisOutlined key="ellipsis" />,
                    // ]}
                  >
                    {this.cutStr(item.content, 50)}
                  </Card>
                </List.Item>
              )}
            />
          </TabPane>
          <TabPane
            tab={
              <span>
                <AppleOutlined />
                Andision's iPhone X
              </span>
            }
            key="1"
          >
            <List
              grid={{ gutter: 16, column: 1 }}
              dataSource={data2}
              renderItem={(item) => (
                <List.Item>
                  <Card size="small" title={item.time}>
                    {item.content}
                  </Card>
                </List.Item>
              )}
            />
          </TabPane>
          <TabPane
            tab={
              <span>
                <AndroidOutlined />
                Andision's HUAWEI Mate 30
              </span>
            }
            key="2"
          >
            <List
              grid={{ gutter: 16, column: 1 }}
              dataSource={data2}
              renderItem={(item) => (
                <List.Item>
                  <Card size="small" title={item.time}>
                    {item.content}
                  </Card>
                </List.Item>
              )}
            />
          </TabPane>
          <TabPane
            tab={
              <span>
                <AndroidOutlined />
                Andision's HUAWEI Mate 31
              </span>
            }
            key="3"
          >
            <List
              grid={{ gutter: 16, column: 1 }}
              dataSource={data2}
              renderItem={(item) => (
                <List.Item>
                  <Card size="small" title={item.time}>
                    {item.content}
                  </Card>
                </List.Item>
              )}
            />
          </TabPane>
          <TabPane
            tab={
              <span>
                <AndroidOutlined />
                Andision's HUAWEI Mate 32
              </span>
            }
            key="4"
          >
            <List
              grid={{ gutter: 16, column: 1 }}
              dataSource={this.state.realData}
              renderItem={(item) => (
                <List.Item>
                  <Card size="small" title={item.time}>
                    {item.content}
                  </Card>
                </List.Item>
              )}
            />
          </TabPane>
        </Tabs>
      </div>
    );
  }
}

export default AirClip;
