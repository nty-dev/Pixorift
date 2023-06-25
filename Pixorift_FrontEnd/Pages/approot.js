import React, {Component} from 'react';
import {KeyboardAvoidingView, TextInput, Platform, StyleSheet, Text, View} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {createAppContainer, createBottomTabNavigator} from 'react-navigation';
import api from './Pixorift/api';
import Profilepage from './Pixorift/profilepage';
import MainPage from './Pixorift/MainPage';
import UpdatePage from './Pixorift/update';
import LBpage from './Pixorift/lb';
import Icon from 'react-native-vector-icons/AntDesign';

const PixoAppRoot = createBottomTabNavigator({
  Quests: {
    screen: MainPage,
    navigationOptions: {
      tabBarLabel: '',
      tabBarIcon: ({ tintColor }) => (
        <Icon name='mail' size={30} color={ tintColor }/>
      )
    }
  },
  Level: {
    screen: Profilepage,
    navigationOptions: {
      tabBarLabel: '',
      tabBarIcon: ({ tintColor }) => (
        <Icon name='barchart' size={30} color={ tintColor }/>
      )
    }
  },
  Update: {
    screen: UpdatePage,
    navigationOptions: {
      tabBarLabel: '',
      tabBarIcon: ({ tintColor }) => (
        <Icon name='user' size={30} color={ tintColor }/>
      )
    }
  },
  Leaderboard: {
    screen: LBpage,
    navigationOptions: {
      tabBarLabel: '',
      tabBarIcon: ({ tintColor }) => (
        <Icon name='Trophy' size={30} color={ tintColor }/>
      )
    }
  },
},
{
  order: ['Quests', 'Level', 'Leaderboard', 'Update'],
  tabBarOptions: {
    activeTintColor: '#253c78',
    inactiveTintColor: '#7c7c7c',
    style: {
      backgroundColor: 'white'
    },
    showIcon: true,
    showLabel: false
  }
}

)

export default createAppContainer(PixoAppRoot);
