import { createOidcAuth, SignInType, LogLevel } from 'vue-auth-oidc'

const authConfig = {
  authority: process.env.VUE_APP_AUTHENTIK_URL,
  clientId: process.env.VUE_APP_AUTHENTIK_CLIENT_ID,
  responseType: 'code',
  scope: 'openid profile email',
  redirectUri: `${window.location.origin}/auth/callback`,
  postLogoutRedirectUri: window.location.origin,
}

const auth = createOidcAuth('mycelium', SignInType.Window, authConfig, console, LogLevel.Debug)

export default auth
