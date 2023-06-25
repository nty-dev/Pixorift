import React, {Component} from 'react';
import {Alert, KeyboardAvoidingView, TextInput, ActivityIndicator, FlatList, AppRegistry, Platform, StyleSheet, Text, View, Dimensions, ScrollView} from 'react-native';
import psts from './stylefolder/profilestyles';
import {Button, Header, Card, Divider} from 'react-native-elements';
import {withNavigation} from 'react-navigation';
import api from './api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Progress from 'react-native-progress';
import loginsts from './stylefolder/loginstyles';
import ss from './stylefolder/appstyles';

var {height, width} = Dimensions.get('window');

class LBpage extends Component{
  constructor(props){
    super(props);
    this.state = {
      lbinfo: [],
    }
  };

  componentDidMount(){
    const {navigation} = this.props;
    this.focusListener = navigation.addListener('didFocus', () => {
      this.lbcall();
    });
    this.lbcall();
    var {height, width} = Dimensions.get('window');
    console.log(height);
  };

  componentWillUnmount(){
    this.focusListener.remove();
  };

  lbcall = async () => {
    await api.getLeaderboard().then((res) => {
      this.setState({lbinfo: res.info});
    });
  };

  lbtitle = (position, username) => {
    var stylemap = {1: [ss.lb1, ss.lbp1], 2: [ss.lb2, ss.lbp2], 3: [ss.lb3, ss.lbp3]};
    if (position < 4) {
      var styleuse = stylemap[position];
    } else {
      var styleuse = [ss.lb, ss.lbp];
    };
    return(
      <View style={ss.lbtitle}>
        <Text style={styleuse[1]}>
          #{position}
        </Text>
        <Text style={styleuse[0]}>
          {username}
        </Text>
        <Text style={{textAlign: 'right', flex: 1}} />
      </View>
    )
  };

  render(){
    return(
      <View style={ss.container}>
        <Header
          containerStyle={ss.headerstyle}
          centerComponent={{text: 'Leaderboard', style: ss.headtext2}}
        />
        <ScrollView>
          <View>
            <FlatList
              data={this.state.lbinfo}

              keyExtractor={(item, index) => index.toString()}
              renderItem={({item}) =>
                  <View>
                    <Card
                      title={this.lbtitle(item.position, item.player)}
                      containerStyle={ss.cardstyle}
                    >
                    	<Divider style={ss.dividerstyle}/>
                      <Text style={ss.leveltext2}>Level: {item.level}</Text>
                      <View style={{justifyContent: 'center', flex: 1}}>
                        <Progress.Bar
                          progress={item.xp/item.full_xp}
                          color='#6b4e71'
                          unfilledColor='#f3afff'
                          borderColor='#231926'
                          width={null}
                          height={height/70}
                          borderRadius={10}
                        />
                      </View>
                    </Card>
                  </View>
              }
            />
          </View>
          <View style={{marginTop: height/35}} />
        </ScrollView>
      </View>
    );
  };
};

export default withNavigation(LBpage);
