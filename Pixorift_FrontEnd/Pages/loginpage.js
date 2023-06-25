import React, {Component} from 'react';
import {ScrollView, ActivityIndicator, Alert, KeyboardAvoidingView, TextInput, Platform, StyleSheet, Text, View, Image, TouchableWithoutFeedback, Keyboard} from 'react-native';
import loginsts from './Pixorift/stylefolder/loginstyles';
import ss from './Pixorift/stylefolder/appstyles';
import {Button, Header} from 'react-native-elements';
import {createSwitchNavigator, createAppContainer} from 'react-navigation';
import api from './Pixorift/api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import AppLoad from './loading';

export default class UserHandlePage extends Component {
  constructor(props){
    super(props);
    this.state = {
      currentpage: 'login'
    };
  };

  SignUpPageCall = () => {
    this.setState({currentpage: 'signup'});
  };

  LoginPageCall = () => {
    this.setState({currentpage: 'login'});
  };

  conditionalrender = () => {
    if (this.state.currentpage === 'login'){
      return(
        <Loginpage
          usercheck={this.props.usercheck}
          SignUpPageCall={this.SignUpPageCall}
        />
      );
    } else if (this.state.currentpage === 'signup') {
      return(
        <Signuppage
          usercheck={this.props.usercheck}
          LoginPageCall={this.LoginPageCall}
        />
      );
    };
  };

  render(){
    return(
      <View style={{flex: 1}}>
        {this.conditionalrender()}
      </View>
    )
  }
}


class Loginpage extends Component {
  constructor(props){
    super(props);
    this.state = {
      error: '',
      keyrender: 'f',
      keyboardstate: 'f',
    };
    this._keyboardDidHide = this._keyboardDidHide.bind(this);
    this._keyboardDidShow = this._keyboardDidShow.bind(this);
  };

  componentDidMount(){
    this.keyboardDidShowListener = Keyboard.addListener(
      'keyboardDidShow',
      this._keyboardDidShow,
    );
    this.keyboardDidHideListener = Keyboard.addListener(
      'keyboardDidHide',
      this._keyboardDidHide,
    );
  };

  componentWillUnmount() {
    this.keyboardDidShowListener.remove();
    this.keyboardDidHideListener.remove();
  };

  _keyboardDidShow(){
    this.setState({keyboardstate: 't'});
  };

  _keyboardDidHide(){
    this.setState({keyboardstate: 'f'});
  };

  logincheck = async () => {
    if (this.state.resstate === 'Success'){
      var Logindate = new Date();
      const LoginInfo = {username: this.state.username, password: this.state.password, token: this.state.usertoken, login: Date.parse(Logindate)};
      await AsyncStorage.setItem('@userinfo', JSON.stringify(LoginInfo)).then(
        () => {
          console.log('Login was successful!');
      }
      ).catch(
        () => {this.setState({
          error: "Can't store account into device AsyncStorage!",
          keyrender: 'f'
        })}
      );
    } else if (this.state.resstate === 'Denied') {
      this.setState({
        error: this.state.errormessage,
        keyrender: 'f',
      });
      Alert.alert('Login Error!', this.state.errormessage);
      this.username.clear();
      this.password.clear();
    }
  };

  unitext = <Text style={loginsts.headtext}>Logging in...</Text>;

  renderkey = () => {
    if (this.state.keyrender === 'f') {
      return (
        <TouchableWithoutFeedback onPress={() => Keyboard.dismiss()}>
        <View>
          <View style={{alignItems: 'center'}}>
            <Image
              source={require('./Pixorift/images/pixorift_logo.png')}
              style={loginsts.logo}
              resizeMode = 'center'
            />
          </View>
          <TextInput
                 ref = {input => {this.username = input}}
                 onChangeText = {(text) => this.setState({username: text})}
                 style={loginsts.logintb}
                 autoCorrect={false}
                 returnKeyType="next"
                 placeholder='Username'
                 placeholderTextColor='rgba(225,225,225,0.7)'
                 />
          <TextInput style={loginsts.logintb}
                ref = {input => {this.password = input}}
                onChangeText = {(text) => this.setState({password: text})}
                autoCorrect={false}
                returnKeyType="go"
                placeholder='Password'
                placeholderTextColor='rgba(225,225,225,0.7)'
                secureTextEntry={true}
                />
          <Button
            title='Login'
            buttonStyle={loginsts.loginbutton}
            onPress = {() => {
              if (this.state.username !== undefined && this.state.password !== undefined) {
                this.setState({keyrender: 't'});
                api.getLogin(this.state.username, this.state.password).then((res) => {
                  this.setState({
                    errormessage: res.error,
                    resstate: res.state,
                    usertoken: res.token,
                  })
                  this.logincheck().then(() => {this.props.usercheck()});
                }).catch(() => {this.setState({keyrender: 'f'}); Alert.alert('Network error!', 'We are unable to connect to Pixorift and log you in!')});
              } else {
                Alert.alert('Login Error!', 'Please enter both a Username and Password!');
              }
            }
            }
          />
        </View>
        </TouchableWithoutFeedback>
      );
    } else {
      return (
        <AppLoad unitext={this.unitext} />
      )
    };
  }

  signupbuttonrender = () => {
    if (this.state.keyboardstate === 'f' && this.state.keyrender === 'f'){
      return(
        <View style={loginsts.signupbutcontain}>
          <Button
            style={loginsts.signup}
            buttonStyle={ss.buttonstyle}
            titleStyle={ss.buttontext}
            title="Don't have an account yet? Sign up."
            onPress={() => {
              this.props.SignUpPageCall();
            }}
          />
        </View>
      )
    };
  };

  render() {
    return(
      <View style={loginsts.loginContainer}>
        {this.renderkey()}
        {this.signupbuttonrender()}
      </View>
    );
  }
}

class Signuppage extends Component {
  constructor(props){
    super(props);
    this.state = {
      currentpage: 'main'
    };
  };

  signupswitch = () => {
    this.setState({currentpage: 'signup'})
  };

  mainswitch = () => {
    this.setState({currentpage: 'main'})
  };

  conditionalrender(){
    if (this.state.currentpage === 'main') {
      return(
        <Signuppage1
          LoginPageCall={this.props.LoginPageCall}
          signupswitch={this.signupswitch}
        />
      )
    } else if (this.state.currentpage === 'signup') {
      return(
        <Signuppage2
          mainswitch={this.mainswitch}
          usercheck={this.props.usercheck}
        />
      )
    }
  };

  render(){
    return(
      <View style={{flex: 1}}>
        {this.conditionalrender()}
      </View>
    )
  }
}

class Signuppage1 extends Component {
  render(){
    return(
      <View style={loginsts.loginContainer}>
        <View style={{alignItems: 'center'}}>
          <Image
            source={require('./Pixorift/images/pixorift_logo.png')}
            style={loginsts.logo}
            resizeMode = 'center'
          />
        </View>
        <Button
          buttonStyle={loginsts.signupbutton}
          title='Sign Up'
          onPress={() => {
            this.props.signupswitch();
          }}
        />
        <View style={loginsts.signupbutcontain}>
          <Button
            style={loginsts.signup}
            title="Already have an account? Sign in."
            titleStyle={ss.buttontext}
            onPress={() => {
              this.props.LoginPageCall();
            }}
            buttonStyle={ss.buttonstyle}
          />
        </View>
      </View>
    )
  }
};

class Signuppage2 extends Component {
  constructor(props){
    super(props);
    this.state = {
      availcheck: 'blancc',
      entry: '',
      submission: false,
    };
  };

  usernameavail = async (username) => {
    api.useravail(username).then((res) => {this.setState({availcheck: res.check})}).catch(() => {this.setState({availcheck: 'failed'})});
  };

  usernamestatus = () => {
    if (this.state.availcheck === 'blancc') {
      return(<Text style={ss.usernameverifytext}/>)
    } else if (this.state.availcheck === 'failed') {
      return(<Text style={ss.usernameverifytext}>Network error! Unable to check username availiability</Text>)
    } else if (this.state.availcheck === 'True') {
      return(<Text style={ss.usernameverifytext}>Username is available!</Text>)
    } else if (this.state.availcheck === 'False') {
      return(<Text style={ss.usernameverifytext}>Username is taken!</Text>)
    } else if (this.state.availcheck === 'process') {
      return(<Text style={ss.usernameverifytext}>Checking...</Text>)
    }
  };

  logincheck = async () => {
    var Logindate = new Date();
    const LoginInfo = {username: this.state.username, password: this.state.password, token: this.state.usertoken, login: Date.parse(Logindate)};
    await AsyncStorage.setItem('@userinfo', JSON.stringify(LoginInfo)).then(
      () => {
        console.log('Login was successful!');
    }
    ).catch(
      () => {this.setState({
        error: "Can't store account into device AsyncStorage!",
        keyrender: 'f'
      })}
    );
  }

  render(){
    return(
      <View style={loginsts.signupContainer}>
          <Header
            containerStyle={ss.headerstyle}
            leftComponent={<BackButton mainswitch = {this.props.mainswitch} />}
            centerComponent={{text: 'Sign Up to Pixorift', style: ss.headtext}}
          />

        <ScrollView>
          {this.usernamestatus()}
          <TextInput
            style={loginsts.logintb}
            returnKeyType='next'
            onChangeText = {(res) => {
              this.setState({availcheck: 'process'});
              if (res !== undefined && res.length !== 0) {
                this.setState({entry: res})
                setTimeout(() => {
                  if (this.state.entry === res){
                    this.usernameavail(res);
                  }
                }, 3000);
              } else {
                this.setState({availcheck: 'blancc'});
              }
            }}
            placeholder='Username'
            editable={!this.state.submission}
          />
          <TextInput
            style={loginsts.logintb}
            returnKeyType ='next'
            onChangeText = {(res) => {this.setState({displayid: res})}}
            placeholder='Display Name'
            editable={!this.state.submission}
          />
          <TextInput
            style={loginsts.logintb}
            returnKeyType = 'next'
            onChangeText = {(res) => {this.setState({email: res})}}
            placeholder='Email'
            editable={!this.state.submission}
          />
          <TextInput
            style={loginsts.logintb}
            returnKeyType = 'next'
            onChangeText = {(res) => {this.setState({fname: res})}}
            placeholder='First Name'
            editable={!this.state.submission}
          />
          <TextInput
            style={loginsts.logintb}
            returnKeyType = 'next'
            onChangeText = {(res) => {this.setState({lname: res})}}
            placeholder='Last Name'
            editable={!this.state.submission}
          />
          <TextInput
            style={loginsts.logintb}
            returnKeyType = 'next'
            secureTextEntry = {true}
            onChangeText = {(res) => {this.setState({password1: res})}}
            placeholder='Password'
            editable={!this.state.submission}
          />
          <TextInput
            style={loginsts.logintb}
            returnKeyType = 'go'
            secureTextEntry = {true}
            onChangeText = {(res) => {this.setState({password2: res})}}
            placeholder='Confirm Password'
            editable={!this.state.submission}
          />
          <Button
            title='Sign Up'
            buttonStyle={loginsts.loginbutton}
            disabled={this.state.submission}
            onPress={() => {
              if (this.state.password1 !== this.state.password2) {
                Alert.alert('Error!', 'Passwords do not match! Please re-enter!');
              } else {
                this.setState({submission: true});
                var submission = {username: this.state.entry, displayid: this.state.displayid, email: this.state.email, first_name: this.state.fname, last_name: this.state.lname, password: this.state.password1};
                api.createUser(submission).then((res) => {
                  if (res.state === 'Denied') {
                    Alert.alert('Error!', JSON.stringify(res.forminfo));
                    this.setState({submission: false});
                  } else if (res.state === 'Success') {
                    this.setState({
                      username: this.state.entry,
                      password: this.state.password1,
                      usertoken: res.token
                    });
                    this.logincheck().then(() => {this.props.usercheck();this.setState({submission:false})});
                }}).catch(() => {Alert.alert('Network error!', 'We are unable to connect to Pixorift and log you in!').then(this.setState({submission: false}))});
              };
            }}
          />
        </ScrollView>
      </View>
    )
  }
}

class BackButton extends Component {
  render(){
    return(
      <Button
        buttonStyle={ss.headerbutton}
        icon={{
          name: 'arrow-back',
          size: 30,
          color: '#2b2d42'
        }}
        onPress={() => {
            this.props.mainswitch();
          }
        }
      />
    )
  }
}
