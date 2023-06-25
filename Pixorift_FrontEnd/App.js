import React, {Component} from 'react';
import {View} from 'react-native';
import PixoRoot from './Pages/root';

export default class App extends Component{
  render(){
    return(
      <View style={{flex:1}}>
        <PixoRoot />
      </View>
    )
  }
}
