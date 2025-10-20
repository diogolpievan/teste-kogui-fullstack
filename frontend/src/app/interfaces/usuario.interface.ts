export interface Usuario {
  IDUsuario: number;
  Nome: string;
  Login: string;
  Email: string;
  DtInclusao: string;
  DtAlteracao: string;
}

export interface LoginRequest {
  login: string;
  senha: string;
}

export interface LoginResponse {
  access_token: string;
  user: Usuario;
}

export interface RegistrarRequest {
  Nome: string;
  Login: string;
  Email: string;
  Senha: string;
}
