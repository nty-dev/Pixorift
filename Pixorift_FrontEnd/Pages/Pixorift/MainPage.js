import React, {Component} from 'react';
import {KeyboardAvoidingView, TextInput, Platform, StyleSheet, Text, View, Alert, ScrollView} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {Button, Header, Card} from 'react-native-elements';
import api from './api';
import loginsts from './stylefolder/loginstyles';
import ss from './stylefolder/appstyles';
import ImagePicker from 'react-native-image-picker';

export default class MainPage extends Component {
  constructor(props){
    super(props);
    this.state = {
      q1: '',
      q2: '',
      q3: '',
      qstate: 'l',
      bstatus: false,
    };
    this._isMounted = false;
    this._refresh = true;
  };

  questcall = async () => {
    await AsyncStorage.getItem('@userinfo').catch((res) => {console.log(res);}).then((res) => {this.setState({apireq: JSON.parse(res)})});
    await api.obtainQuests(this.state.apireq.username, this.state.apireq.token).catch((res) => {console.log(res);}).then((res) => {
      if (res.status === 'Success') {
        this.setState({
          q1: res.Quest.Quest1,
          q2: res.Quest.Quest2,
          q3: res.Quest.Quest3,
          qstate: 'd'
        });
        this.state.q1.key = '1';
        this.state.q2.key = '2';
        this.state.q3.key = '3';
        this._refresh = true;
        this.timer(this.state.q1);
        this.timer(this.state.q2);
        this.timer(this.state.q3);
      } else if (res.status === 'Denied') {
        Alert.alert('Error', 'API denied core request, please relog into Pixorift.')
      };
    });
  };

  timer = (questobj) => {
    if (questobj.state === false && this._isMounted === true && this._refresh === true) {
      if (questobj.Time.m === 0 && questobj.Time.s === 0) {
        this.questcall();
        questobj.countdown = false;
      } else if (questobj.Time.s === 0) {
        questobj.Time.m = questobj.Time.m - 1
        questobj.Time.s = 59
        setTimeout(() => {this.timer(questobj);}, 1000);
        this.setState({test: 'e'});
      } else {
        questobj.Time.s = questobj.Time.s - 1
        setTimeout(() => {this.timer(questobj);}, 1000);
        this.setState({test: 'e'});
      }
    };
  };

  elongate(number){
    var ret = number.toString();
    if (ret.length === 1) {
      var rt = '0' + ret;
      return rt;
    } else {
      return ret;
    }
  }

  checkquest = (questobj) => {
    if (questobj.state === true) {
      return (
        <View>
          <Text>
            Current Item: {questobj.Quest}
          </Text>
          <Text />
          <Button
            title='Submit'
            buttonStyle={ss.submitButton}
            titleStyle={ss.buttontext2}
            onPress={() => {
              this.cameraCall(questobj.key);
            }}
            disabled={this.state.bstatus}
          />
        </View>
      )
    } else if (questobj.state === false) {
      return (
        <View>
          <Text>
            Time Remaining: {questobj.Time.h}:{this.elongate(questobj.Time.m)}:{this.elongate(questobj.Time.s)}
          </Text>
        </View>
      )
    } else if (questobj.state === 'submit') {
      return(
        <View>
          <Text>
            Submitting....
          </Text>
        </View>
      )
    }
  };

  questfunc = (qo) => {
    if (this.state.qstate === 'l') {
      return(
        <Text>Loading....</Text>
      )
    } else if (this.state.qstate === 'd') {
      return (
        this.checkquest(qo)
      )
    }
  };

  componentDidMount(){
    this._isMounted = true;
    this.questcall();
  };

  componentWillUnmount(){
    this._isMounted = false;
  };

  cameraCall = async (questno) => {
    var options = {}
    ImagePicker.launchCamera(options, image => {
      this.camera2Call(questno, image);
    })
  };

  camera2Call = async (questno, image) => {
    this.setState({bstatus: true});
    await AsyncStorage.getItem('@userinfo').catch((res) => {console.log(res);}).then((res) => {this.setState({apireq: JSON.parse(res)})});
    this._refresh = false;
    if (questno === '1') {
      var temp = this.state.q1;
      temp.state = 'submit';
      this.setState({q1: temp});
    } else if (questno === '2') {
      var temp = this.state.q2;
      temp.state = 'submit';
      this.setState({q2: temp});
    } else if (questno === '3') {
      var temp = this.state.q2;
      temp.state = 'submit';
      this.setState({q2: temp});
    };
    api.submitQuest(this.state.apireq.username, this.state.apireq.token, questno, 'data:' + image.type + ';base64,' + image.data).catch((res) => {console.log(res);}).then((res) => {
      if (res.status === 'Denied' || res.status === 'Failed' || res.status === undefined) {
        Alert.alert('Error!', 'Unable to submit picture to Pixorift!');
      } else if (res.status === 'Success') {
        if (res.Quest === 'Failed') {
          Alert.alert('Quest Failed!', res.Reason);
        } else if (res.Quest === 'Success') {
          Alert.alert(res.reason, 'You gained ' + res.XP_Gain + ' experience!');
        }
      };
      this.setState({bstatus: false});
      this.questcall();
    });
  }

  render(){
    return(
      <View style={ss.container}>
        <Header
          centerComponent={{text: 'Current Quests', style: ss.headtext2}}
          containerStyle={ss.headerstyle}
        />
        <ScrollView>
          <Card title='Quest 1'>
            {this.questfunc(this.state.q1)}
          </Card>
          <Card title='Quest 2'>
            {this.questfunc(this.state.q2)}
          </Card>
          <Card title='Quest 3'>
            {this.questfunc(this.state.q3)}
          </Card>
        </ScrollView>
      </View>
    )
  }
};
