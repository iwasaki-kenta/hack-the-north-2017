import React, { Component } from 'react';
import { Picker, List, FlatList, Text, StyleSheet, View, TextInput, Button, Alert } from 'react-native';
import firebase from 'firebase';
import Dimensions from 'Dimensions';

class Login extends Component {
    constructor(props){
        super(props);
        this.state = {
            email: '',
            password: ''
        };
    }

    componentDidMount(){
        this.componentDidUpdate();
    }
    componentDidUpdate(){
        if(this.props.content && this.state.lastContent !== this.props.content){
            this.setState({lastContent: this.props.content, imageurl: null});
            this.getData(this.props.content);
        }
    }
    firebaseLogin(e, email, password, nav){
        console.log(firebase.auth().currentUser);
        firebase.auth().signInWithEmailAndPassword(email, password).catch(function(error) {
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
    }
    render() {
        return (
            <View style={{width: Dimensions.get('window').width, padding: 25, paddingTop: 60}}>
                <Text style={styles.title}>Log In</Text>
                <Text keyboardType='email-address'>Email</Text>
                <TextInput
                    style={{height: 40, backgroundColor: '#fff', padding: 5}}
                    placeholder="Enter your email"
                    onChangeText={(email) => this.setState({email})}
                    value={this.state.email}
                />

                <Text>Password</Text>
                <TextInput
                    secureTextEntry={true}
                    style={{height: 40, backgroundColor: '#fff', padding: 5}}
                    placeholder="Enter your password."
                    onChangeText={(password) => this.setState({password})}
                    value={this.state.password}
                />

                <Button
                    onPress={(e) => this.firebaseLogin(e, this.state.email, this.state.password, this.props)}
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

export default Login;
