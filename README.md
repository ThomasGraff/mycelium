<div align="center">
  <img src="frontend/mycelium/src/assets/logo.png" alt="Mycelium Logo" width="150"/>
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
    <kbd><h2 align="center">[ INITIALIZATION_SEQUENCE ]</h2></kbd>
    <br><br>


<code>> Prerequisites</code>

<table>
  <tr>
    <td align="center" width="50%">
      <img src="https://img.icons8.com/color/48/000000/docker.png" width="30"/>
      <br />
      <b>> Local Usage</b>
      <br />
      <ul align="left">
        <li>Docker and Docker Compose</li>
        <li>Git</li>
      </ul>
    </td>
    <td align="center" width="50%">
      <img src="https://img.icons8.com/color/48/000000/code.png" width="30"/>
      <br />
      <b>> Development</b>
      <br />
      <ul align="left">
        <li>Node.js (v18+)</li>
        <li>Yarn (preferred over npm)</li>
        <li>Python (v3.10+)</li>
        <li>Poetry</li>
        <li>Git</li>
      </ul>
    </td>
  </tr>
</table>

<br>

<code>> Environment Configuration</code>

<br>

<table>
  <tr>
    <th>Variable</th>
    <th>Required</th>
    <th>Default</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>PG_PASS</code></td>
    <td>✅</td>
    <td>-</td>
    <td>PostgreSQL password for Authentik</td>
  </tr>
  <tr>
    <td><code>FRONTEND_PORT</code></td>
    <td>❌</td>
    <td>8080</td>
    <td>Frontend application port</td>
  </tr>
  <tr>
    <td><code>BACKEND_PORT</code></td>
    <td>❌</td>
    <td>8000</td>
    <td>Backend API port</td>
  </tr>
  <tr>
    <td><code>AUTHENTIK_PORT_HTTP</code></td>
    <td>❌</td>
    <td>9000</td>
    <td>Authentik HTTP port</td>
  </tr>
  <tr>
    <td><code>AUTHENTIK_PORT_HTTPS</code></td>
    <td>❌</td>
    <td>9443</td>
    <td>Authentik HTTPS port</td>
  </tr>
</table>

<div align="center">
  <i>.env file required for next step</i>
</div>
<br><br>
<code>> One-Line Setup</code>
<br><br>

```bash
git clone https://github.com/ThomasGraff/mycelium.git && cd mycelium && docker-compose up -d
```


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
