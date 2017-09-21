import React from 'react';
import { Platform } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { TabNavigator, TabBarBottom } from 'react-navigation';

import Colors from '../constants/Colors';

import EntriesScreen from '../screens/EntriesScreen';
import ProfileScreen from '../screens/ProfileScreen';
// import CameraScreen from '../screens/CameraScreen';

export default TabNavigator(
  {
    Entries: {
      screen: EntriesScreen,
    },
    // Camera: {
    //   screen: CameraScreen,
    // },
    Profile: {
      screen: ProfileScreen,
    },
  },
  {
    navigationOptions: ({ navigation }) => ({
      tabBarIcon: ({ focused }) => {
        const { routeName } = navigation.state;
        let iconName;
        switch (routeName) {
          case 'Entries':
            iconName = Platform.OS === 'ios'
              ? `ios-home${focused ? '' : '-outline'}`
              : 'md-home';
            break;
        //   case 'Camera':
        //     iconName = Platform.OS === 'ios'
        //       ? `ios-camera${focused ? '' : '-outline'}`
        //       : 'md-camera';
        //     break;
          case 'Profile':
            iconName = Platform.OS === 'ios'
              ? `ios-person${focused ? '' : '-outline'}`
              : 'md-person';
        }
        return (
          <Ionicons
            name={iconName}
            size={28}
            style={{ marginBottom: -3 }}
            color={focused ? Colors.tabIconSelected : Colors.tabIconDefault}
          />
        );
      },
    }),
    tabBarComponent: TabBarBottom,
    tabBarPosition: 'bottom',
    animationEnabled: false,
    swipeEnabled: false,
  }
);
