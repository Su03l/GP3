import 'package:flutter/material.dart';

class LanguagePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('langage'),
      ),
      body: Center(
        child: Text('Here you can change the langauge'),
      ),
    );
  }
}