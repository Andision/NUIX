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
import Launcher from './Launcher';
import DevicePanel from './DevicePanel';

const { TabPane } = Tabs;

class Homepage extends React.Component {
  constructor(props) {
    super(props);
    this.LauncherRef = React.createRef();
    this.DevicePanelRef = React.createRef();
    this.state = {};
  }

  render() {
    return (
      <div className="my-app">
        <Tabs defaultActiveKey="1">
          <TabPane tab="应用列表" key="1">
            <Launcher ref={this.LauncherRef}/>
          </TabPane>
          <TabPane tab="设备管理" key="2">
            <DevicePanel ref={this.DevicePanelRef}/>
          </TabPane>
        </Tabs>
      </div>
    );
  }
}

export default Homepage;
