import React, {Component} from 'react';
import {KeyboardAvoidingView, TextInput, Platform, StyleSheet, Text, View, ActivityIndicator, Image} from 'react-native';
import loginsts from './Pixorift/stylefolder/loginstyles';

export default class AppLoad extends Component {
  render() {
    return(
      <View style={loginsts.loginContainer}>
        <View style={{alignItems: 'center'}}>
          <Image
            source={require('./Pixorift/images/pixorift_logo.png')}
            style={loginsts.logo}
            resizeMode = 'center'
            />
          </View>
        <ActivityIndicator
            color = '#266DD3'
            size = 'large'
        />
        <View>
          {this.props.unitext}
        </View>
      </View>
    )
  };
};
