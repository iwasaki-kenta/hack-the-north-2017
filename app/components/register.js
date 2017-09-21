import React, { Component } from 'react';
import { Picker, List, FlatList, Text, StyleSheet, View, TextInput, Button, Alert } from 'react-native';
import firebase from 'firebase';
import Dimensions from 'Dimensions';

class Register extends Component {
    constructor(props){
        super(props);
        this.state = {
            email : '',
            password : '',
            password2 : '',
            passwordsMatch : false,
        };
    }
    firebaseRegister(e, email, password, password2, nav){
        if (this.state.password == this.state.password2){
            firebase.auth().createUserWithEmailAndPassword(email, password).catch(function(error) {
                var errorCode = error.code;
                var errorMessage = error.message;
                Alert.alert(
                    'Uh oh!',
                    errorMessage,
                    [
                        {text: 'OK', onPress: () => console.log('OK Pressed')},
                    ],
                    { cancelable: false }
                )

            });
        } else{
            Alert.alert(
                'Uh oh!',
                'Passwords do not match!',
                [
                    {text: ':c'},
                ],
                { cancelable: false }
            )
        }
    };
    password(password2){
        if (this.state.password == this.state.password2){
            this.state = {
                passwordsMatch: true
            }
        }
        this.setState({password2})
    }
    render() {

        return (
            <View style={{width: Dimensions.get('window').width, padding: 25, paddingTop: 60}}>
                <Text style={styles.title}>Register</Text>
                <Text keyboardType='email-address'>Email</Text>
                <TextInput
                    style={{height: 40, backgroundColor: '#fff', padding: 5}}
                    placeholder="Enter your email"
                    onChangeText={(email) => this.setState({email})}
                    value={this.state.email}
                />

                <Text>Password</Text>
                <TextInput
                    style={{height: 40, backgroundColor: '#fff', padding: 5}}
                    placeholder="Enter your password."
                    secureTextEntry={true}
                    onChangeText={(password) => this.setState({password})}
                    value={this.state.password}
                />
                <Text>Confirm</Text>
                <TextInput
                    style={{height: 40, backgroundColor: '#fff', padding: 5}}
                    placeholder="Enter your password."
                    onChangeText={(password2) => this.setState({password2})}
                    value={this.state.password2}
                    secureTextEntry={true}
                />
                <Button
                    onPress={(e) => this.firebaseRegister(e, this.state.email, this.state.password, this.state.password2, this.props)}
                    title="Let's Go!"
                    color="#4CAF50"
                />
            </View>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        padding: 10,
        alignItems: 'center',
    },
    title: {
        fontSize: 25,
    }

});


export default Register;
