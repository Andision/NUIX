import {
  Col,
  Divider,
  Row,
  Tabs,
  Card,
  List,
  Button,
  Avatar,
  Badge,
} from 'antd';
import React from 'react';
import { BrowserRouter as Router, Route, NavLink } from 'react-router-dom';

import {
  AndroidOutlined,
  AppleOutlined,
  WindowsOutlined,
  DeleteOutlined,
  DisconnectOutlined,
  EllipsisOutlined,
  SettingOutlined,
} from '@ant-design/icons';

import './Launcher.css';

// import WidthUseNavigate from '../js/widthUseNavigate';

const { Meta } = Card;

class Launcher extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      app_list: [
        {
          id: 0,
          title: "Andision's ThinkPad X390",
          description: '',
          icon: 'https://s1.ax1x.com/2022/08/17/vBeTNn.png',
          badge_count: 2,
        },
        {
          id: 1,
          title: "Andision's iPhone X",
          description: '',
          icon: 'https://s1.ax1x.com/2022/08/16/v0JfQs.png',
          badge_count: 1,
        },
        {
          id: 2,
          title: "Andision's HUAWEI Mate 30",
          description: '',
          icon: 'https://s1.ax1x.com/2022/08/17/vBelm4.png',
          badge_count: 5,
        },
        {
          id: 3,
          title: "Andision's HUAWEI Mate 31",
          description: '',
          icon: 'https://s1.ax1x.com/2022/08/17/vBelm4.png',
          badge_count: 12,
        },
      ],
    };
  }

  handleCardClick = (event, id, path) => {
    // const navigate = useNavigate();
    console.log('click app id= ', id, 'path= ', path);
    console.log('event= ', event.target.nodeName);

    // if (event.target.nodeName == 'DIV' || event.target.nodeName == 'IMG') {
    //   window.location.href = `#${path}`;
    // } else {
    //   console.log('event= ', event.target.nodeName);
    // }
  };

  render() {
    return (
      <div className="my-app">
        <Row
          gutter={[
            { xs: 16, sm: 20, md: 24, lg: 32 },
            { xs: 16, sm: 20, md: 24, lg: 32 },
          ]}
        >
          {this.state.app_list.map((item) => {
            return (
              <Col
                key={item.id}
                className="gutter-row"
                span={6}
                xs={24}
                sm={12}
                md={8}
                lg={6}
                xl={6}
              >
                <Badge count={item.badge_count} overflowCount={99}>
                  <Card
                    onClick={(e) => this.handleCardClick(e, item.id, item.path)}
                    className="app-block"
                    cover={
                      <img
                        alt="icon"
                        src={item.icon}
                        width={262}
                        height={159}
                      />
                    }
                    hoverable
                    actions={[
                      <SettingOutlined key="setting" />,
                      <DisconnectOutlined key="edit" />,
                      <EllipsisOutlined key="ellipsis" />,
                    ]}
                  >
                    <Meta title={item.title} description={item.description} />
                  </Card>
                </Badge>
              </Col>
            );
          })}
        </Row>
      </div>
    );
  }
}

export default Launcher;

// // 使用高阶组件包裹当前类组件
// const NavigateCompont = WidthUseNavigate(Launcher);
// // 导出包裹后的类组件
// export default NavigateCompont;
