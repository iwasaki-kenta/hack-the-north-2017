import React from 'react';
import { WebBrowser } from 'expo';
import { View, StyleSheet, Text, Image, TextInput, Button } from 'react-native';

import { MonoText } from '../components/StyledText';
import firebase from 'firebase';
import Dimensions from 'Dimensions';

export default class SettingsScreen extends React.Component {
  static navigationOptions = {
    title: 'Profile',
  };

  constructor(props){
      super(props);
      this.state = {
          user: firebase.auth().currentUser,
      };
  }

  logout(){
      firebase.auth().signOut().then(function() {
        // Sign-out successful.
      }, function(error) {
        // An error happened.
      });
  }
  render() {
      console.log(this.state.user);
    return(
        <View style={{width: Dimensions.get('window').width, padding: 25}}>
            <Text fontWeight='bold'>Email: </Text><Text>{this.state.user.email}</Text>
            <Button
              onPress={() => this.logout()}
              title="Logout"
              color="#4CAF50"
            />
            </View>
    );
  }

}

const styles = StyleSheet.create({
    title: {
        fontSize: 25,
    }
});
