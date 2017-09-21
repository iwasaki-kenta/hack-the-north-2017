import React from 'react';
import firebase from 'firebase';

import { AppRegistry, FlatList, StyleSheet, Text, View, Container, Image, Modal, Button, TouchableWithoutFeedback, ScrollView, Dimensions } from 'react-native';
import { ExpoLinksView } from '@expo/samples';
const config = require('../config.json');
import request from "superagent";

var {height, width} = Dimensions.get('window');
export default class LinksScreen extends React.Component {
    static navigationOptions = {
        title: 'Links',
    };

    constructor(props){
        // console.log(data);
    	super(props);
    	this.state = {
    		items: [{text: "This one is very long NTHontuh oentuh oentu hnoet huntoeh unoteh unoethu onetuh oentuh oeNTH"}, {text: "NTHNTH"}, {text: "NTHNTH"}, {text: ""}, {text: "New document"}],
            modalVisible: false,
            modalContent: {},
            dataSource: []
    	};
        this.itemsRef = firebase.database().ref("/notes/");
    }
    getAutocomplete(text, latitude, longitude, callback) {
      request.get("http://ec2-35-182-16-224.ca-central-1.compute.amazonaws.com/api/getSearchResults?userLocation=" + latitude + "," + longitude + "&query=" + text).end(callback);
    }

    getData(text, latitude, longitude){
      this.getAutocomplete(text, latitude, longitude, (err, result) => {
          data = JSON.parse(result.text)
       if (data){
           this.state.suggestions = data;
       }
       this.setState({suggestions: data})
      });
      }
    listenForItems(itemsRef) {
    itemsRef.on('value', (snap) => {
      var items = [];
      snap.forEach((child) => {
        child = JSON.parse(JSON.stringify(child));
        console.log(child);
        if (child["category"] == -1){
            var category = "No category"
        } else if (child["category"] == 0){
            var category = "Education"
        }else if (child["category"] == 1){
            var category = "Legal"
        }else if (child["category"] == 2){
            var category = "Nutrition"
        }
        var data = {
            text: child["note"],
            image: child["image"],
            category: category
        }
        items.push(data);
        console.log(data)
      });

      this.setState({
        dataSource: items
      });
    });
  }

  componentDidMount() {
          this.listenForItems(this.itemsRef);
          console.log("componentDidMount")
        }
      setModalVisible(visible) {
        this.setState({modalVisible: visible});
      }

    select(e, item){
        this.setState({
            modalContent: {
                text: item.text,
                image: item.image,
            }
        })
        console.log(this.state.modalContent)
        this.setModalVisible(true)

    }
    render() {
        return (
            <View>

            <View>
                <Text style={styles.title}>{this.state.title}</Text>

                <ScrollView >
                <FlatList
                  data={this.state.dataSource}
                  renderItem={({item}) => (
                      <TouchableWithoutFeedback
                        onPress={(e) => this.select(e, item)}
                        >
                        <View style={{ flexDirection:'row', flexWrap:'wrap', borderBottomColor: 'grey',borderBottomWidth: 1, padding: 5}}>
                            <Image
                                style={{height: 50, width: 50}}
                                source={{uri: item.image}} />
                            <Text style={{padding: 5}}>
                                {item.text}
                            </Text>
                        </View>
                        </TouchableWithoutFeedback>

                  )}                   style={styles.select}
                />
                </ScrollView>
            </View>
            <Modal
              animationType="slide"
              transparent={false}
              visible={this.state.modalVisible}
              onRequestClose={() => {alert("Modal has been closed.")}}
              >
             <View style={{marginTop: 22}}>
              <View              style={{padding: 15, alignItems: 'center'}}>
                <Text style={styles.title}>Details</Text>

                <Image
                    style={{width: 300, height: 200}}
                    source={{uri: this.state.modalContent.image}} />
                <Text>
                {this.state.modalContent.text}
                </Text>
                <Button
                onPress={() => {
                  this.setModalVisible(!this.state.modalVisible)
                }}
                  title="Hide"
                  color="#4CAF50"
                  text="Hide"
                  />
              </View>
             </View>
            </Modal>
            </View>

        );
    }
}

const styles = StyleSheet.create({
    container: {
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  justifyContent: 'flex-end',
  alignItems: 'center',
},
map: {
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
},
    title: {
        backgroundColor: '#FFFFFF',
        padding: 10,
        textAlign: 'center',
        fontSize: 25
    },
    top: {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        flex: 1
    },
    select: {
        backgroundColor: '#FFFFFF',
        padding: 10,
        flexDirection: 'row'
    },
    item: {
        borderWidth: 1,
        borderColor: '#d6d7da',
    },

  modalContent: {
    backgroundColor: 'white',
    padding: 22,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 4,
    borderColor: 'rgba(0, 0, 0, 0.1)',
  },
  bottomModal: {
    justifyContent: 'flex-end',
    margin: 0,
  },
});
