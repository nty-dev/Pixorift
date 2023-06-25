import React, {Component} from 'react';
import {Alert, KeyboardAvoidingView, Divider, TextInput, ActivityIndicator, FlatList, AppRegistry, Platform, StyleSheet, Text, View, Dimensions, ScrollView} from 'react-native';
import psts from './stylefolder/profilestyles';
import {Button, Header} from 'react-native-elements';
import {withNavigation} from 'react-navigation';
import api from './api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Progress from 'react-native-progress';
import loginsts from './stylefolder/loginstyles';
import ss from './stylefolder/appstyles';

class UpdatePage extends Component {
  constructor(props){
    super(props);
    this.state = {
      navigator: '1',
      load: true,
      userdetails: '',
    };
    this._runcall = false;
  };

  usercall = async () => {
    await AsyncStorage.getItem('@userinfo').catch((res) => {console.log(res);}).then((res) => {this.setState({apireq: JSON.parse(res)})});
    api.getUserInfo(this.state.apireq.username, this.state.apireq.token).then((res) => {this.setState({userdetails: res})});
  };

  updatecall = async (info) => {
    await AsyncStorage.getItem('@userinfo').catch((res) => {console.log(res);}).then((res) => {this.setState({apireq: JSON.parse(res)})});
    info.oldusername = this.state.apireq.username;
    info.Auth = this.state.apireq.token;
    api.updateUser(info).then((res) => {return(res)});
  };

  componentDidMount(){
    const {navigation} = this.props;
    this.focusListener = navigation.addListener('didFocus', () => {
      if (this._runcall === false){
        this._runcall = true;
        this.usercall().then(() => {this._runcall = false;});
      }
    });
    this.usercall().then(this.setState({load: false}));
  };

  componentWillUnmount(){
    this.focusListener.remove();
  };

  maincall = () => {
    this.setState({
      navigator: '1'
    });
  };

  passmaincall = () => {
    this.setState({
      navigator: '1'
    });
    Alert.alert('Password Info', 'Password changed successfully!');
  }

  passcall = () => {
    this.setState({
      navigator: '2'
    });
  };

  delcall = () => {
    this.setState({
      navigator: '3'
    });
  };

  logout = async () => {
    await AsyncStorage.getItem('@userinfo').catch((res) => {console.log(res);}).then((res) => {
      const Userinfo = JSON.parse(res);
      api.logoutUser(Userinfo.token).then((res) => {
        if (res.state === 'Success') {
          console.log(res.user.concat(' logged out!'));
        };
      });
    });
    await AsyncStorage.removeItem('@userinfo').catch((res) => {console.log(res)}).then(() => {console.log('User removed from AsyncStorage!');}).then(() => {
      this.props.screenProps.usercheck();
    });
  };

  conditionalrender(){
    if (this.state.navigator === '1'){
      return (
        <UpdateMain
          passcall={this.passcall}
          delcall={this.delcall}
          userdetails={this.state.userdetails}
          load={this.state.load}
          logout={this.logout}
          updatecall={this.updatecall}
          usercall={this.usercall}
        />
      );
    } else if (this.state.navigator === '2'){
      return (
        <ChangePass
          maincall={this.maincall}
          passmaincall={this.passmaincall}
        />
      )
    } else if (this.state.navigator === '3'){
      return (
        <DeleteAcc
          maincall={this.maincall}
          usercheck={this.props.screenProps.usercheck}
        />
      )
    }
  };

  render(){
    return(
      <View style={{flex:1}}>
        {this.conditionalrender()}
      </View>
    );
  };
};

export default withNavigation(UpdatePage);

class UpdateMain extends Component{
  constructor(props){
    super(props);
    this.state = {
      editable: false,
      editscreen: false,
      logout: false,
      updatebutton: false,
      load: this.props.load,
      userdetails: this.props.userdetails,
      username: this.props.userdetails.username,
      displayid: this.props.userdetails.displayid,
      email: this.props.userdetails.email,
      lname: this.props.userdetails.last_name,
      fname: this.props.userdetails.first_name
    };
  };

  userstatecall(){
    this.setState({
      userdetails: this.props.userdetails,
      username: this.props.userdetails.username,
      displayid: this.props.userdetails.displayid,
      email: this.props.userdetails.email,
      lname: this.props.userdetails.last_name,
      fname: this.props.userdetails.first_name
    })
  }

  componentDidUpdate(){
    if (this.state.load !== this.props.load){
      this.setState({load: this.props.load})
    };
    if (this.state.userdetails !== this.props.userdetails){
      this.userstatecall();
    }
  };

  updatecall = async (info) => {
    await AsyncStorage.getItem('@userinfo').catch((res) => {console.log(res);}).then((res) => {
      this.setState({apireq: JSON.parse(res)});
      info.append('oldusername', this.state.apireq.username);
      info.append('Auth', this.state.apireq.token);
    });
    await api.updateUser(info).then((res) => {this.setState({updateresponse: res})}).catch(() => {this.setState({updateresponse: {res: 'Denied'}})});
  };

  updateUserInfo = async () => {
    await AsyncStorage.getItem('@userinfo').catch((res) => {console.log(res);}).then((res) => {this.setState({ui: JSON.parse(res)});});
    this.state.ui.username = this.state.username;
    await AsyncStorage.setItem('@userinfo', JSON.stringify(this.state.ui)).catch((res) => {console.log(res)});
  };

  buttoncondition(){
    if (this.state.editscreen === true) {
      return(
        <View>
          <Button
            title='Update'
            buttonStyle={ss.clickbutton}
            disabled={this.state.updatebutton}
            onPress={() => {
              this.setState({editable: false, updatebutton: true});
              var submission = new FormData();
              submission.append('username', this.state.username);
              submission.append('displayid', this.state.displayid);
              submission.append('email', this.state.email);
              submission.append('first_name', this.state.fname);
              submission.append('last_name', this.state.lname);
              this.updatecall(submission).then(() => {
                var res = this.state.updateresponse;
                if (res.state === 'Denied') {
                  Alert.alert('Update Error!', JSON.stringify(res.forminfo));
                  this.setState({updatebutton: false, editscreen: false});
                  this.userstatecall();
                } else if (res.state === 'Success') {
                  this.updateUserInfo().then(() => {
                    this.props.usercall().then(() => {
                      this.userstatecall();
                      Alert.alert('Success', 'User Information Updated!');
                      this.setState({updatebutton: false, editscreen: false});
                    });
                  });
                }
              })
            }}
          />
          <Button
            title='Cancel'
            buttonStyle={ss.deletebutton}
            disabled={this.state.updatebutton}
            onPress={() => {
              this.setState({
                editable: false,
                editscreen: false,
                updatebutton: false
              });
              this.userstatecall();
            }}
          />
        </View>
      )
    } else {
      return(
        <View>
          <Button
            title='Update Info'
            buttonStyle={ss.updatebutton}
            onPress={() => {
              this.setState({editable: true, editscreen: true});
            }}
          />
          <Button
            title='Change Password'
            buttonStyle={ss.updatebutton}
            onPress={() => {
              this.props.passcall();
            }}
          />
          <Button
            title='Log Out'
            buttonStyle={ss.clickbutton}
            disabled={this.state.logout}
            onPress={() => {
              this.setState({logout: true});
              this.props.logout().then(() => {this.setState({logout: false})});
            }}
          />
          <Button
            title='Delete Account'
            buttonStyle={ss.deletebutton}
            onPress={() => {
              this.props.delcall();
            }}
          />
        </View>
      )
    }
  }

  conditionalrender(){
    if (this.state.load === true) {
     return(
       <View style={loginsts.loginContainer}>
         <ActivityIndicator
             color = '#266DD3'
             size = 'large'
         />
         <Text style={ss.loadtext}>Loading User Information...</Text>
       </View>
     )
   } else if (this.state.load === false){
      return(
        <ScrollView>
          <Text style={ss.updatetext}>Username</Text>
          <TextInput
            style={loginsts.logintb}
            returnKeyType ='next'
            onChangeText = {(res) => {this.setState({username: res})}}
            value={this.state.username}
            editable={this.state.editable}
          />
          <Text style={ss.updatetext}>Display Name</Text>
          <TextInput
            style={loginsts.logintb}
            returnKeyType ='next'
            onChangeText = {(res) => {this.setState({displayid: res})}}
            value={this.state.displayid}
            editable={this.state.editable}
          />
          <Text style={ss.updatetext}>Email Address</Text>
          <TextInput
            style={loginsts.logintb}
            returnKeyType ='next'
            onChangeText = {(res) => {this.setState({email: res})}}
            value={this.state.email}
            editable={this.state.editable}
          />
          <Text style={ss.updatetext}>First Name</Text>
          <TextInput
            style={loginsts.logintb}
            returnKeyType ='next'
            onChangeText = {(res) => {this.setState({fname: res})}}
            value={this.state.fname}
            editable={this.state.editable}
          />
          <Text style={ss.updatetext}>Last Name</Text>
          <TextInput
            style={loginsts.logintb}
            returnKeyType ='next'
            onChangeText = {(res) => {this.setState({lname: res})}}
            value={this.state.lname}
            editable={this.state.editable}
          />
          {this.buttoncondition()}
        </ScrollView>
      )
    }
  }

  render(){
    return(
      <View style={ss.container}>
        <Header
          containerStyle={ss.headerstyle}
          centerComponent={{text: 'User Information', style: ss.headtext2}}
        />
        {this.conditionalrender()}
      </View>
    );
  };
};

class ChangePass extends Component{
  constructor(props){
    super(props);
    this.state = {
      call: false,
    }
  };

  changepassword = async () => {
    await AsyncStorage.getItem('@userinfo').catch((res) => {console.log(res);}).then((res) => {this.setState({apireq: JSON.parse(res)})});
    api.changePassword(this.state.apireq.username, this.state.apireq.token, this.state.oldpassword, this.state.password1, this.state.password2).then((res) => {
      if (res.state === 'Denied') {
        Alert.alert('Password Change Error!', res.error);
        this.setState({call: false});
        this.oldpassword.clear();
        this.password1.clear();
        this.password2.clear();
      } else if (res.state === 'Success') {
        this.updatepassword().then(() => {
          this.setState({call: false});
          this.props.passmaincall();
        });
      }
    })
  }

  updatepassword = async () => {
    await AsyncStorage.getItem('@userinfo').catch((res) => {console.log(res);}).then((res) => {this.setState({ui: JSON.parse(res)});});
    this.state.ui.password = this.state.password1;
    await AsyncStorage.setItem('@userinfo', JSON.stringify(this.state.ui)).catch((res) => {console.log(res)});
  };

  render(){
    return(
      <View style={ss.container}>
        <Header
          containerStyle={ss.headerstyle}
          centerComponent={{text: 'Change Password', style: ss.headtext2}}
          leftComponent={
            <Button
              buttonStyle={ss.headerbutton}
              icon={{
                name: 'arrow-back',
                size: 30,
                color: '#2b2d42'
              }}
              onPress={() => {
                  this.props.maincall();
                }
              }
            />
          }
        />
        <ScrollView style={ss.container}>
          <Text style={ss.suretext}>
            Are you sure you want to change your password?
          </Text>
          <TextInput
            editable={!this.state.call}
            ref = {input => {this.oldpassword = input}}
            onChangeText = {(text) => this.setState({oldpassword: text})}
            style={loginsts.logintb}
            autoCorrect={false}
            returnKeyType="next"
            placeholder='Old Password'
            placeholderTextColor='rgba(225,225,225,0.7)'
            secureTextEntry={true}
          />
          <TextInput
            editable={!this.state.call}
            ref = {input => {this.password1 = input}}
            onChangeText = {(text) => this.setState({password1: text})}
            style={loginsts.logintb}
            autoCorrect={false}
            returnKeyType="next"
            placeholder='New Password'
            placeholderTextColor='rgba(225,225,225,0.7)'
            secureTextEntry={true}
          />
          <TextInput
            editable={!this.state.call}
            style={loginsts.logintb}
            ref = {input => {this.password2 = input}}
            onChangeText = {(text) => this.setState({password2: text})}
            autoCorrect={false}
            returnKeyType="go"
            placeholder='Confirm New Password'
            placeholderTextColor='rgba(225,225,225,0.7)'
            secureTextEntry={true}
          />
          <Button
            title='Change Password'
            disabled={this.state.call}
            buttonStyle={ss.updatebutton}
            onPress={() => {
              if (this.state.oldpassword != undefined && this.state.password1 != undefined && this.state.password2 != undefined) {
                this.setState({call: true});
                this.changepassword();
              } else {
                Alert.alert('Password Change Error!', 'Password fields cannot be blank!')
              }
            }}
          />
          <Button
            title='Cancel'
            disabled={this.state.call}
            buttonStyle={ss.clickbutton}
            onPress={() => {
              this.props.maincall();
            }}
          />
        </ScrollView>
      </View>
    );
  }
};

class DeleteAcc extends Component{
  constructor(props){
    super(props);
    this.state = {
      call : false,
    }
  };

  delete_user = async () => {
    await AsyncStorage.getItem('@userinfo').catch((res) => {console.log(res);}).then((res) => {this.setState({apireq: JSON.parse(res)})});
    await api.deleteUser(this.state.username, this.state.apireq.token, this.state.password).then((res) => {
      if (res.state === 'Denied'){
        Alert.alert('Deletion Failure', res.error);
        this.username.clear();
        this.password.clear();
        this.setState({call: false});
      } else if (res.state === 'success') {
        this.deletion();
      };

    })
  };

  deletion = async () => {
    await AsyncStorage.removeItem('@userinfo').catch((res) => {console.log(res)});
    this.props.usercheck();
    this.setState({call: false});
  };

  render(){
    return(
      <View style={ss.container}>
        <Header
          containerStyle={ss.headerstyle}
          centerComponent={{text: 'ACCOUNT DELETION', style: ss.headtext3}}
          leftComponent={
            <Button
              buttonStyle={ss.headerbutton}
              icon={{
                name: 'arrow-back',
                size: 30,
                color: '#2b2d42'
              }}
              onPress={() => {
                  this.props.maincall();
                }
              }
            />
          }
        />
        <ScrollView style={ss.container}>
          <Text style={ss.suretext}>
            Are you sure you want to delete your account?
          </Text>
          <Text style={ss.smalltext}>
            Enter Username and Password to Continue
          </Text>
          <TextInput
            editable={!this.state.call}
            ref = {input => {this.username = input}}
            onChangeText = {(text) => this.setState({username: text})}
            style={loginsts.logintb}
            autoCorrect={false}
            returnKeyType="next"
            placeholder='Username'
            placeholderTextColor='rgba(225,225,225,0.7)'
          />
          <TextInput
            editable={!this.state.call}
            style={loginsts.logintb}
            ref = {input => {this.password = input}}
            onChangeText = {(text) => this.setState({password: text})}
            autoCorrect={false}
            returnKeyType="go"
            placeholder='Password'
            placeholderTextColor='rgba(225,225,225,0.7)'
            secureTextEntry={true}
          />
          <Button
            title='Delete Account'
            disabled={this.state.call}
            buttonStyle={ss.deletebutton}
            onPress={() => {
              if (this.state.username !== undefined && this.state.password !== undefined) {
                this.setState({call: true});
                this.delete_user();
              } else {
                Alert.alert('Deletion Failed', 'Username or Password blank!');
              }
            }}
          />
          <Button
            title='Cancel'
            disabled={this.state.call}
            buttonStyle={ss.clickbutton}
            onPress={() => {
              this.props.maincall();
            }}
          />
        </ScrollView>
      </View>
    );
  }
}
