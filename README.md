<div align="center">
  <img src="https://images.weserv.nl/?url=https://github.com/myceliumAI/mycelium/blob/main/mycelium/src/assets/logo.png?raw=true&fit=cover&mask=circle&maxage=7d" alt="Mycelium Logo" width="150"/>
  <br><br>
  
  <div>
    <kbd><h1 align="center">[ MYCELIUM ]</h1></kbd>
    <br><br>
    <table align="center">
      <tr>
        <td align="left"><code>[LICENSE]</code></td>
        <td>
          <a href="https://www.gnu.org/licenses/agpl-3.0">
            <img src="https://img.shields.io/badge/License-AGPL_v3-blue.svg" alt="License: AGPL v3"/>
          </a>
        </td>
      </tr>
      <tr>
        <td align="left"><code>[METRICS]</code></td>
        <td>
          <a href="https://github.com/ThomasGraff/mycelium/stargazers">
            <img src="https://img.shields.io/github/stars/ThomasGraff/mycelium.svg" alt="GitHub Stars"/>
          </a>
          <a href="https://github.com/ThomasGraff/mycelium/network">
            <img src="https://img.shields.io/github/forks/ThomasGraff/mycelium.svg" alt="GitHub Forks"/>
          </a>
          <a href="https://github.com/ThomasGraff/mycelium/issues">
            <img src="https://img.shields.io/github/issues/ThomasGraff/mycelium.svg" alt="GitHub Issues"/>
          </a>
        </td>
      </tr>
      <tr>
        <td align="left"><code>[UTILS]</code></td>
        <td>
          <a href="#documentation">
            <code>DOCS</code>
          </a>
          &nbsp;&nbsp;|&nbsp;&nbsp;
          <a href="https://github.com/ThomasGraff/mycelium/issues/new?template=bug_report.md">
            <code>BUGS</code>
          </a>
          &nbsp;&nbsp;|&nbsp;&nbsp;
          <a href="https://github.com/ThomasGraff/mycelium/issues/new?template=feature_request.md">
            <code>FEATURES</code>
          </a>
        </td>
      </tr>
      <tr>
        <td align="left"><code>[DESCRIPTION]</code></td>
        <td><i>
          A powerful platform designed to simplify the creation and management<br>
          of Data Contracts, bridging systems for seamless data ingestion.</i>
        </td>
      </tr>
    </table>
  </div>
</div>

<div align="center">│</div>
<div align="center">▼</div>
<br>
<div align="center">
  <div>
    <kbd><h2 align="center">[ CORE_FEATURES ]</h2></kbd>
    <br><br>
    <table>
      <tr>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/artificial-intelligence.png" width="30"/>
          <br />
          <b><span style="color: #00ff00;">></span> AI-Powered Contracts</b>
          <br />
          Auto-generate data contracts using advanced LLM technology
        </td>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/speed.png" width="30"/>
          <br />
          <b><span style="color: #00ff00;">></span> Fast Ingestion</b>
          <br />
          Automated configuration and streamlined pipeline setup
        </td>
      </tr>
      <tr>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/dashboard.png" width="30"/>
          <br />
          <b><span style="color: #00ff00;">></span> Smart Visualization</b>
          <br />
          Track contracts and map data sources in real-time
        </td>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/collaboration.png" width="30"/>
          <br />
          <b><span style="color: #00ff00;">></span> Team Collaboration</b>
          <br />
          Unite teams with centralized contract management
        </td>
      </tr>
    </table>
  </div>
</div>

<div align="center">│</div>
<div align="center">▼</div>
<br>
<div align="center">
  <div>
    <kbd><h2 align="center">[ DEPENDENCY CHECK ]</h2></kbd>
    <br>
    <table>
      <tr>
        <td align="center" width="50%">
          <img src="https://img.icons8.com/color/48/000000/docker.png" width="30"/>
          <br />
          <b>Production</b>
          <br />
          <kbd><code>make check-prod</code></kbd>
        </td>
        <td align="center" width="50%">
          <img src="https://img.icons8.com/color/48/000000/code.png" width="30"/>
          <br />
          <b>Development</b>
          <br />
          <kbd><code>make check-dev</code></kbd>
        </td>
      </tr>
    </table>
  </div>
</div>

<div align="center">│</div>
<div align="center">▼</div>
<br>
<div align="center">
  <div>
    <kbd><h2 align="center">[ ENVIRONMENT SETUP ]</h2></kbd>
    <br>
    <table>
      <tr>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/settings.png" width="30"/>
          <br />
          <kbd><code>make setup-env</code></kbd>
        </td>
      </tr>
    </table>
    <details>
      <summary>
        <b> Click to View Configuration Details</b>
      </summary>
      <br>
      <table>
        <tr>
          <th colspan="5" align="center">Authentik Configuration</th>
        </tr>
        <tr>
          <th>Variable</th>
          <th>Required</th>
          <th>Default</th>
          <th>Auto-generation method</th>
          <th>Description</th>
        </tr>
        <tr>
          <td><code>AUTHENTIK_PORT</code></td>
          <td>❌</td>
          <td>9000</td>
          <td>-</td>
          <td>Port on which Authentik server will listen</td>
        </tr>
        <tr>
          <td><code>AUTHENTIK_HOST</code></td>
          <td>❌</td>
          <td>localhost</td>
          <td>-</td>
          <td>Hostname for the Authentik service in the Docker network</td>
        </tr>
        <tr>
          <td><code>AUTHENTIK_BOOTSTRAP_EMAIL</code></td>
          <td>❌</td>
          <td>admin@localhost</td>
          <td>-</td>
          <td>Email for the admin user</td>
        </tr>
        <tr>
          <td><code>AUTHENTIK_SECRET_KEY</code></td>
          <td>✅</td>
          <td>-</td>
          <td><code>openssl rand -base64 60 | tr -d '\n'</code></td>
          <td>Secret key for JWT token generation</td>
        </tr>
        <tr>
          <td><code>AUTHENTIK_ADMIN_PASSWORD</code></td>
          <td>✅</td>
          <td>-</td>
          <td><code>openssl rand -base64 16</code></td>
          <td>Password for the admin user</td>
        </tr>
        <tr>
          <td><code>AUTHENTIK_ADMIN_TOKEN</code></td>
          <td>✅</td>
          <td>-</td>
          <td><code>openssl rand -hex 32</code></td>
          <td>API token for the admin user</td>
        </tr>
        <tr>
          <td><code>AUTHENTIK_CLIENT_ID</code></td>
          <td>✅</td>
          <td>-</td>
          <td>Via Authentik API</td>
          <td>Client ID for the backend service</td>
        </tr>
        <tr>
          <td><code>AUTHENTIK_CLIENT_SECRET</code></td>
          <td>✅</td>
          <td>-</td>
          <td>Via Authentik API</td>
          <td>Client secret for the backend service</td>
        </tr>
        <tr>
          <td><code>PG_USER</code></td>
          <td>❌</td>
          <td>authentik</td>
          <td>-</td>
          <td>PostgreSQL user</td>
        </tr>
        <tr>
          <td><code>PG_DB</code></td>
          <td>❌</td>
          <td>authentik</td>
          <td>-</td>
          <td>PostgreSQL database name</td>
        </tr>
        <tr>
          <td><code>PG_PASS</code></td>
          <td>✅</td>
          <td>-</td>
          <td><code>openssl rand -base64 36 | tr -d '\n'</code></td>
          <td>PostgreSQL password for Authentik database</td>
        </tr>
        <tr>
          <th colspan="5" align="center">Backend Configuration</th>
        </tr>
        <tr>
          <td><code>BACKEND_PORT</code></td>
          <td>❌</td>
          <td>8000</td>
          <td>-</td>
          <td>Port on which the FastAPI backend service will listen</td>
        </tr>
        <tr>
          <td><code>BACKEND_HOST</code></td>
          <td>❌</td>
          <td>localhost</td>
          <td>-</td>
          <td>Hostname for the backend service in the Docker network</td>
        </tr>
        <tr>
          <td><code>DATABASE_URL</code></td>
          <td>❌</td>
          <td>sqlite:///./app/database/mycelium.db</td>
          <td>-</td>
          <td>SQLite database connection string for the application</td>
        </tr>
        <tr>
          <th colspan="5" align="center">Frontend Configuration</th>
        </tr>
        <tr>
          <td><code>FRONTEND_PORT</code></td>
          <td>❌</td>
          <td>8080</td>
          <td>-</td>
          <td>Port on which the Vue.js frontend will be served</td>
        </tr>
        <tr>
          <td><code>FRONTEND_HOST</code></td>
          <td>❌</td>
          <td>localhost</td>
          <td>-</td>
          <td>Hostname for the frontend service in the Docker network</td>
        </tr>
      </table>
      <small align="center">
        For complete configuration options, refer to .env.example
      </small>
    </details>
  </div>
</div>

<div align="center">│</div>
<div align="center">▼</div>
<br>
<div align="center">
  <div>
    <kbd><h2 align="center">[ DEPLOYMENT ]</h2></kbd>
    <br>
    <table>
      <tr>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/launch-box.png" width="30"/>
          <br>
          <kbd><code>make launch</code></kbd>
          <br>
          <small>Deploys Auth, Frontend, and Backend services</small>
        </td>
      </tr>
    </table>
    <details>
      <summary>
        <b> Click to View Individual Service Commands</b>
      </summary>
      <br>
      <table>
        <tr>
          <td align="center">
            <img src="https://img.icons8.com/color/48/000000/password.png" width="25"/>
            <br>
            <kbd><code>make auth</code></kbd>
            <br>
            <small>Authentication</small>
          </td>
          <td align="center">
            <img src="https://img.icons8.com/color/48/000000/web.png" width="25"/>
            <br>
            <kbd><code>make front</code></kbd>
            <br>
            <small>Frontend</small>
          </td>
          <td align="center">
            <img src="https://img.icons8.com/color/48/000000/api.png" width="25"/>
            <br>
            <kbd><code>make back</code></kbd>
            <br>
            <small>Backend</small>
          </td>
        </tr>
      </table>
    </details>
  </div>
</div>

<div align="center">│</div>
<div align="center">▼</div>
<br>
<div align="center">
  <div>
    <kbd><h2 align="center">[ CONTRIBUTION_PROTOCOL ]</h2></kbd>
    <br><br>
    <table>
      <tr>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/code-fork.png" width="30"/>
          <br />
          <b>Fork</b>
          <br />
          Fork the repository
        </td>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/split.png" width="30"/>
          <br />
          <b>Branch</b>
          <br />
          <code>git checkout -b feat/YourFeature</code>
        </td>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/commit-git.png" width="30"/>
          <br />
          <b>Commit</b>
          <br />
          <code>git commit -m 'Add feature'</code>
        </td>
      </tr>
      <tr>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/upload-to-cloud.png" width="30"/>
          <br />
          <b>Push</b>
          <br />
          <code>git push origin feat/YourFeature</code>
        </td>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/pull-request.png" width="30"/>
          <br />
          <b>Pull Request</b>
          <br />
          Open a PR on GitHub
        </td>
        <td align="center">
          <img src="https://img.icons8.com/color/48/000000/communication.png" width="30"/>
          <br />
          <b>Discuss</b>
          <br />
          Engage in review process
        </td>
      </tr>
    </table>
  </div>
</div>
