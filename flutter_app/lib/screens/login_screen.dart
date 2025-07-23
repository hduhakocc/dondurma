import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  String _username = '';
  String _password = '';
  bool _loading = false;
  String? _error;

  @override
  Widget build(BuildContext context) {
    final auth = Provider.of<AuthService>(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Giriş Yap')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextFormField(
                decoration: const InputDecoration(labelText: 'Kullanıcı Adı'),
                onChanged: (v) => _username = v,
                validator: (v) => v == null || v.isEmpty ? 'Zorunlu alan' : null,
              ),
              TextFormField(
                decoration: const InputDecoration(labelText: 'Şifre'),
                obscureText: true,
                onChanged: (v) => _password = v,
                validator: (v) => v == null || v.isEmpty ? 'Zorunlu alan' : null,
              ),
              const SizedBox(height: 20),
              if (_error != null) ...[
                Text(_error!, style: const TextStyle(color: Colors.red)),
                const SizedBox(height: 10),
              ],
              _loading
                  ? const CircularProgressIndicator()
                  : ElevatedButton(
                      onPressed: () async {
                        if (_formKey.currentState!.validate()) {
                          setState(() { _loading = true; _error = null; });
                          final success = await auth.login(_username, _password);
                          if (!success) {
                            setState(() { _error = 'Giriş başarısız'; });
                          }
                          setState(() { _loading = false; });
                        }
                      },
                      child: const Text('Giriş Yap'),
                    ),
            ],
          ),
        ),
      ),
    );
  }
}
