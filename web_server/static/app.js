const app = Vue.createApp({
  template: `

    <div class="hub" v-for='hubs in hubs_data'>
        <div class="port" v-for="hub in hubs">
            <div  class="disconnected" v-if="!Object.keys(ports_data).some(key => key.substring(1) === hub.substring(1))"> 
                <p class="device_section">Desconectado</p>
                <p class="device_section">-</p>
                <p class="device_section">-</p>
                <p class="device_section">-</p>
         
            </div>
            <div class="connected" v-if="Object.keys(ports_data).some(key => key.substring(1) === hub.substring(1))">
                <p class="device_section">{{select_partial_match(hub)["name"] }}</p>                
                <div class="mount-points device_section" v-if='Object.keys(select_partial_match(hub)["children"]).length > 0'>
                    <div class="children-container"  v-for="children in select_partial_match(hub)['children']">
                        <p class="text-left">{{children[0]}}</p>
                        <p class="text-left">└> {{"/"+children[1].split("/")[children[1].split("/").length -1 ]}} ─ {{children[2]}}</p>
                    
                    </div>
                   
                </div>
                
                <p class="device_section usb_3" v-if='select_partial_match(hub)["usb_version_3"]'>USB 3.x</p>
                <p class="device_section " v-if='!select_partial_match(hub)["usb_version_3"]'>USB 2.0</p>
                <button>Transferir</button>
            </div>
        </div>
    </div>
    `,
  data() {
    return {
      fetchData: null, // Initialize with null or an initial value
      hubs_data: null,
      ports_data: null,
    };
  },
  mounted() {
    this.fetchDataFromServer();
    // setInterval(this.fetchDataFromServer, 5000);
  },
  methods: {
    async fetchDataFromServer() {
      // Fetch data from the server or any source
      // Update the fetchData property
      this.fetchData = await fetchDataFromServer();
      this.hubs_data = this.fetchData[0];
      this.ports_data = this.fetchData[1];

      console.log(this.hubs_data);
      console.log(this.ports_data);
    },
    select_partial_match(specific_identifier) {
      main_identifier = "1" + specific_identifier.substring(1);
      for (port_identifier in this.ports_data) {
        if ("1" + port_identifier.substring(1) === specific_identifier) {
          return this.ports_data[port_identifier];
        }
      }
    },
  },
});
async function fetchDataFromServer() {
  const [ports_data_response, hubs_data_response] = await Promise.all([
    fetch("/get_per_usb_data"),
    fetch("/get_hubs"),
  ]);
  const ports_data = await ports_data_response.json();
  const hubs_data = await hubs_data_response.json();
  return [hubs_data, ports_data];
}

app.mount("#app");

// <p>{{ ports_data[hub]["name"] }}</p>
// <p>{{ ports_data[hub]["size"] }}</p>
// <p>{{ ports_data[hub]["mount_points"] }}</p>
// <p v-if='ports_data[hub]["usb_version_3"]'>USB 3</p>
// <p v-if='!ports_data[hub]["usb_version_3"]'>USB 2</p>

// udisksctl mount -b /dev/sdb1 --no-user-interaction
// gunicorn --bind 0.0.0.0:5000 wsgi:app
