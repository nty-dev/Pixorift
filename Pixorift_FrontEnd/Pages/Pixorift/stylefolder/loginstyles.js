import { StyleSheet, Dimensions } from 'react-native';

var {height, width} = Dimensions.get('window');

const loginsts = StyleSheet.create({
    logintb: {
        //flex: 1,
        borderWidth: 1,
        borderColor: '#000000',
        padding: height/70,
        marginBottom: height/35,
        height: height/17,
        marginHorizontal: width/8,
        borderRadius: 20,
        backgroundColor: "#ffffff",
    },
    loginContainer:{
        flex: 5,
        justifyContent: 'center',
        backgroundColor: '#E0FBFC'
    },
    signupContainer:{
        flex: 5,
        backgroundColor: '#E0FBFC',
    },
    loginbutton:{
        backgroundColor: '#161925',
        padding: height/70,
        marginHorizontal: width/8,
        borderRadius: 20
    },
    logo: {
      marginBottom: height/35,
    },
    headtext: {
  	     color: '#395C6B',
  	     fontSize: 20,
         textAlign: 'center',
         marginBottom: height/35
    },
    signuptext: {
  	     color: '#395C6B',
  	     fontSize: 20,
         textAlign: 'center',
         marginBottom: height/35,
         alignItems: 'center'
    },
    errortext: {
         color: '#FB3640',
         fontSize: height/34,
         textAlign:'center'
    },
    signupbutcontain: {
         //color: '#161925',
         position: 'absolute',
         left: 0,
         right: 0,
         bottom: 0,
         alignItems: 'stretch',
         //justifyContent: 'flex-end',
         flexDirection: 'column',
    },
    signup: {
        height: height/70,
        flex: 1,
        position: 'absolute'
    },
    signupbutton:{
        backgroundColor: '#161925',
        padding: height/70,
        marginHorizontal: height/5,
        borderRadius: 10
    },
});

export default loginsts;
