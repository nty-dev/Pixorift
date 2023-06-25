import { StyleSheet, Dimensions } from 'react-native';

var {height, width} = Dimensions.get('window');

const ss = StyleSheet.create({
    headerstyle: {
      backgroundColor: '#b1dae2',
      borderBottomWidth: 1,
      borderBottomColor: '#000000'
    },
    loadtext: {
      color: '#2b2d42',
      fontSize: height/35,
      textAlign: 'center'
    },
    headtext: {
      color: '#2b2d42',
      fontSize: height/27,
      fontWeight: 'bold',
      textAlign: 'center'
    },
    headtext2: {
      color: '#161925',
      fontSize: height/34,
      fontWeight: 'bold',
      textAlign: 'center'
    },
    headtext3: {
      color: '#F71735',
      fontSize: height/34,
      fontWeight: 'bold',
      textAlign: 'center'
    },
    leveltext: {
      color: '#24222b',
      fontSize: height/34,
      textAlign: 'center',
      paddingTop: height/15,
      paddingBottom: height/15
    },
    headerbutton: {
      backgroundColor: '#b1dae2',
    },
    usernameverifytext: {
      textAlign: 'center',
      fontSize: height/57,
      color: '#757273',
    },
    suretext: {
      fontSize: height/30,
      marginHorizontal: width/8,
      color: '#161925',
      fontWeight: '500',
      textAlign: 'center',
      marginBottom: height/35,
      marginTop: height/10
    },
    smalltext:{
      fontSize: height/50,
      marginHorizontal: width/8,
      color: '#757273',
      textAlign: 'center',
      marginBottom: height/35,
    },
    updatetext:{
      fontSize: height/35,
      marginHorizontal: width/8,
      color: '#757273',
      fontWeight: '500',
    },
    buttonstyle: {
      borderRadius: 0,
      borderTopWidth: 1,
      borderColor: '#000000',
      backgroundColor: '#E0FBFC'
    },
    buttonstyle2: {
      borderWidth: 1,
      borderColor: '#000000',
      backgroundColor: '#270722',
    },
    stretchContainer: {
      paddingTop: height/20,
      alignItems: 'stretch'
    },
    submitButton: {
      backgroundColor: '#b1dae2',
      borderWidth: 0.5,
      borderColor: '#000000'
    },
    textbox: {
      paddingBottom: 0
    },
    buttontext: {
      color: '#6b5e62',
      textAlign: 'center'
    },
    circletext: {
      color: '#141414',
      fontWeight: 'bold',
      fontSize: width/5
    },
    buttontext2: {
      color: '#161925',
      textAlign: 'center'
    },
    container: {
      backgroundColor: '#E0FBFC',
      flex: 1,
    },
    container2: {
      backgroundColor: '#E0FBFC',
      flex: 1,
      alignItems: 'center',
    },
    clickbutton:{
        backgroundColor: '#161925',
        padding: height/70,
        marginHorizontal: width/8,
        borderRadius: 20,
        marginBottom: height/35,
    },
    updatebutton:{
        backgroundColor: '#697216',
        padding: height/70,
        marginHorizontal: width/8,
        borderRadius: 20,
        marginBottom: height/35,
    },
    deletebutton:{
        backgroundColor: '#CC4143',
        padding: height/70,
        marginHorizontal: width/8,
        borderRadius: 20,
        marginBottom: height/35
    },
    lb: {
      color: '#000100',
      fontSize: height/35,
      fontWeight: '500',
      textAlign: 'center',
      flex: 1
    },
    lb1: {
      color: '#AF9500',
      fontSize: height/35,
      fontWeight: '500',
      textAlign: 'center',
      flex: 1
    },
    lb2: {
      color: '#B4B4B4',
      fontSize: height/35,
      fontWeight: '500',
      textAlign: 'center',
      flex: 1
    },
    lb3: {
      color: '#6A3805',
      fontSize: height/35,
      fontWeight: '500',
      textAlign: 'center',
      flex: 1
    },
    lbp: {
      color: '#000100',
      fontSize: height/35,
      fontWeight: 'bold',
      textAlign: 'left',
      flex: 1
    },
    lbp1: {
      color: '#AF9500',
      fontSize: height/35,
      fontWeight: 'bold',
      textAlign: 'left',
      flex: 1
    },
    lbp2: {
      color: '#B4B4B4',
      fontSize: height/35,
      fontWeight: 'bold',
      textAlign: 'left',
      flex: 1
    },
    lbp3: {
      color: '#6A3805',
      fontSize: height/35,
      fontWeight: 'bold',
      textAlign: 'left',
      flex: 1
    },
    leveltext2: {
      color: '#000100',
      fontSize: height/40,
      fontWeight: '300',
      textAlign: 'center',
      flex: 1
    },
    lbtitle: {
      flexDirection: 'row',
      justifyContent: 'space-around',
      flex: 1
    },
    dividerstyle: {
      backgroundColor: '#000000',
      paddingVertical: height/1000,
      borderRadius: 10,
      marginVertical: height/75,
    },
    cardstyle: {
      borderWidth: 1,
      borderColor: '#E6ECF1',
      marginTop: height/35,
      marginHorizontal: width/35,
      flex: 1
    }
});

export default ss;
