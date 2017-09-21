import React from 'react';
import { Platform, StatusBar, StyleSheet, View } from 'react-native';
import { AppLoading, Asset, Font } from 'expo';
import { Ionicons } from '@expo/vector-icons';
import RootNavigation from './navigation/RootNavigation';
import LoginScreen from './screens/LoginScreen'

import firebase from 'firebase';

const config = require('./config.json');


export default class App extends React.Component {

    constructor(props) {
        super(props);

        firebase.initializeApp({
            apiKey: config.FIREBASE_API_KEY,
            authDomain: config.FIREBASE_AUTH_DOMAIN,
            databaseURL: config.FIREBASE_DB_URL,
            projectId: config.FIREBASE_PROJ_ID,
            storageBucket: config.FIREBASE_STORAGE_BUCKET,
            messagingSenderId: config.FIREBASE_MESSENGER_SENDING_ID
        });
        this.state = {
            signedIn: firebase.auth().currentUser,
            session: null
        };
    }

    componentDidMount() {
        const ctx = this;
        firebase.auth().onAuthStateChanged(function(user) {
            if (user) {
                ctx.setState({signedIn: true});
            } else {
                ctx.setState({signedIn: false});
            }
        });
    }

    load(key) {
        this.setState({ session: key });
    }
    exit() {
        this.setState({ session: null });
    }

    state = {
        assetsAreLoaded: false,
    };

    componentWillMount() {
        this._loadAssetsAsync();
    }

  render() {
    if (!this.state.assetsAreLoaded && !this.props.skipLoadingScreen) {
      return <AppLoading />;
  } else if(!this.state.signedIn){
      console.log("Not logged in");
      return(<LoginScreen/>)
  }
    else {
      return (
        <View style={styles.container}>
          {Platform.OS === 'ios' && <StatusBar barStyle="default" />}
          {Platform.OS === 'android' &&
            <View style={styles.statusBarUnderlay} />}
          <RootNavigation/>
        </View>
      );
    }
  }

  async _loadAssetsAsync() {
    try {
      await Promise.all([
        Asset.loadAsync([
          require('./assets/images/robot-dev.png'),
          require('./assets/images/robot-prod.png'),
        ]),
        Font.loadAsync([
          // This is the font that we are using for our tab bar
          Ionicons.font,
          // We include SpaceMono because we use it in HomeScreen.js. Feel free
          // to remove this if you are not using it in your app
          { 'space-mono': require('./assets/fonts/SpaceMono-Regular.ttf') },
        ]),
      ]);
    } catch (e) {
      // In this case, you might want to report the error to your error
      // reporting service, for example Sentry
      console.warn(
        'There was an error caching assets (see: App.js), perhaps due to a ' +
          'network timeout, so we skipped caching. Reload the app to try again.'
      );
      console.log(e);
    } finally {
      this.setState({ assetsAreLoaded: true });
    }
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  statusBarUnderlay: {
    height: 24,
    backgroundColor: 'rgba(0,0,0,0.2)',
  },
});
