// Copyright 2020 Robert Cecil. All rights reserved.
// Use of this source code is governed by a MIT license that can be
// found in the LICENSE file.

import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class ControllerState extends State<Controller> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Controller stuff'),
        actions: <Widget>[
          // Add 3 lines from here...
          IconButton(icon: Icon(Icons.list), onPressed: _null),
        ], // ... to here.
      ),
      body: Center(
          child: Text('Placeholder'),
        ),
    );
  }


  void _null() {
   return;
  }

}

class Controller extends StatefulWidget {
  @override
  ControllerState createState() => ControllerState();
}




class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Controller',
      home: Scaffold(
        appBar: AppBar(
          title: Text('Controller'),
        ),
        body: Center(
          child: Controller(),
        ),
      ),
    );
  }
}