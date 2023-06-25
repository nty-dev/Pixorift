import React, {Component} from 'react';
import {KeyboardAvoidingView, Divider, TextInput, ActivityIndicator, FlatList, AppRegistry, Platform, StyleSheet, Text, View, Dimensions} from 'react-native';
import psts from './stylefolder/profilestyles';
import {Button, Header} from 'react-native-elements';
import {withNavigation} from 'react-navigation';
import api from './api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Progress from 'react-native-progress';
import loginsts from './stylefolder/loginstyles';
import ss from './stylefolder/appstyles';

var {height, width} = Dimensions.get('window');

class Profilepage extends Component{
  constructor(props){
    super(props);
    this.state = {
      userdetails: '',
      playerinfo: '',
      progress: 0,
      pload: true,
      uload: true
    };
    this._runcallp = false,
    this._runcallq = false;
  };

  usercall = async () => {
    await AsyncStorage.getItem('@userinfo').then((res) => {this.setState({apireq: JSON.parse(res)})});
    api.getUserInfo(this.state.apireq.username, this.state.apireq.token).then((res) => {this.setState({userdetails: res})});
  };

  playercall = async () => {
    await AsyncStorage.getItem('@userinfo').then((res) => {this.setState({apireq: JSON.parse(res)})});
    api.playerInfo(this.state.apireq.username, this.state.apireq.token).then((res) => {
      this.setState({playerinfo: res});
      this.setState({progress: this.state.playerinfo.XP/this.state.playerinfo.full_xp});
    });
  };


  componentDidMount(){
    const {navigation} = this.props;
    this.focusListener = navigation.addListener('didFocus', () => {
      if (this._runcallp === false && this._runcallq === false){
        this._runcallp = true;
        this._runcallq = false;
        this.playercall().then(() => {this._runcallp = false;});
        this.usercall().then(() => {this._runcallq = false;});
      }

    });
    this.usercall().then(() => {this.setState({uload: false})});
    this.playercall().then(() => {this.setState({pload: false})});
  };

  componentWillUnmount(){
    this.focusListener.remove();
  };

  conditionalrender(){
    if (this.state.pload === true || this.state.uload === true) {
      return(
        <View style={loginsts.loginContainer}>
          <ActivityIndicator
              color = '#266DD3'
              size = 'large'
          />
          <Text style={ss.loadtext}>Loading User Information...</Text>
        </View>
      )
    } else {
      return(
        <View style={ss.container2}>
          <Text style={ss.leveltext}> {this.state.userdetails.displayid}'s Current Level</Text>
          <Progress.Circle
            size={width/10*7}
            thickness={width/10}
            progress={this.state.progress}
            showsText={true}
            color='#594157'
            borderWidth={0}
            unfilledColor='#E0FBFC'
            fill='#ecce8e'
            textStyle={ss.circletext}
            formatText={() => {return(this.state.playerinfo.Level)}}
          />
        </View>
      )
    }
  }

  render() {
    return(
      <View style={ss.container}>
        <Header
          containerStyle={ss.headerstyle}
          centerComponent={{text: 'User Progress', style: ss.headtext2}}
        />
        {this.conditionalrender()}
      </View>
    )
  }
};

export default withNavigation(Profilepage);
