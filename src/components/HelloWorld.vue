<template>
  <!-- <p v-if="loginState">Hola</p> -->
  <login v-if="loginState" v-on:validate="getLoginState($event)"></login>
  <v-data-table
    v-else
    :headers="headers"
    :items="postulanteTable"
    sort-by="Nombre"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>Postulantes Vivekonecta</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <!-- <template v-slot:activator="{ on }">
            <v-btn color="primary" dark class="mb-2" v-on="on">New Item</v-btn>
          </template> -->
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.name" label="Nombre"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.email" label="Correo"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.phone" label="Teléfono"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.register" label="Registro"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.experience" label="Experiencia"></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <!-- <template v-slot:item.action="{ item }">
      <v-icon small class="mr-2" @click="editItem(item)">edit</v-icon>
      <v-icon small @click="deleteItem(item)">delete</v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">Reset</v-btn>
    </template> -->
  </v-data-table>
</template>

<script>
import firebase from "firebase";
import login from "./login.vue";

export default {
  name: "HelloWorld",
  components: {
    login
  },

  data: () => ({
    postulantes: [],
    postulanteTable: [],
    postulantesInfo: {},
    postulantesExp: {},
    postulantesProf: {},
    loginState: true,
    dialog: false,
    headers: [
      {
        text: "Nombre y apellido",
        align: "left",
        sortable: false,
        value: "name"
      },
      { text: "Correo", value: "email" },
      { text: "Teléfono", value: "phone" },
      { text: "Registro", value: "register" },
      { text: "Experiencia", value: "experience" },
      { text: "Actions", value: "action", sortable: false }
    ],
    desserts: [],
    editedIndex: -1,
    editedItem: {
      name: "",
      email: "",
      phone: "",
      register: "",
      experience: ""
    },
    defaultItem: {
      name: "",
      email: "",
      phone: "",
      register: "",
      experience: ""
    }
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    }
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  created() {
    this.initialize();
    this.writeUserData();
    this.writeUserExp();
    this.writeUserProf();
  },
  mounted() {},

  methods: {
    initialize() {
      this.desserts = [
        {
          name: "Frozen Yogurt",
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0
        },
        {
          name: "Ice cream sandwich",
          calories: 237,
          fat: 9.0,
          carbs: 37,
          protein: 4.3
        },
        {
          name: "Eclair",
          calories: 262,
          fat: 16.0,
          carbs: 23,
          protein: 6.0
        },
        {
          name: "Cupcake",
          calories: 305,
          fat: 3.7,
          carbs: 67,
          protein: 4.3
        },
        {
          name: "Gingerbread",
          calories: 356,
          fat: 16.0,
          carbs: 49,
          protein: 3.9
        },
        {
          name: "Jelly bean",
          calories: 375,
          fat: 0.0,
          carbs: 94,
          protein: 0.0
        },
        {
          name: "Lollipop",
          calories: 392,
          fat: 0.2,
          carbs: 98,
          protein: 0
        },
        {
          name: "Honeycomb",
          calories: 408,
          fat: 3.2,
          carbs: 87,
          protein: 6.5
        },
        {
          name: "Donut",
          calories: 452,
          fat: 25.0,
          carbs: 51,
          protein: 4.9
        },
        {
          name: "KitKat",
          calories: 518,
          fat: 26.0,
          carbs: 65,
          protein: 7
        }
      ];
    },

    editItem(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      const index = this.desserts.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.desserts.splice(index, 1);
    },

    close() {
      this.dialog = false;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.desserts[this.editedIndex], this.editedItem);
      } else {
        this.desserts.push(this.editedItem);
      }
      this.close();
    },
    writeUserData() {
      let postulantes = firebase.database().ref("POSTULANTES");
      postulantes.on("value", this.getPostulant, this.dataUserErr);
    },
    getPostulant(data) {
      this.postulantesInfo = data.val();
      console.log(this.postulantesInfo);
    },
    dataUserErr(err) {
      console.log("error");
      console.log(err);
    },
    writeUserExp() {
      let postulantesExp = firebase.database().ref("DATOS_EXPERIENCIA");
      postulantesExp.on("value", this.getPostulantExp, this.dataUserExpErr);
    },
    getPostulantExp(data) {
      this.postulantesExp = data.val();
      console.log(this.postulantesExp);
    },
    dataUserExpErr(err) {
      console.log("error");
      console.log(err);
    },
    writeUserProf() {
      let postulantesProf = firebase.database().ref("DATOS_PROFESIONALES");
      postulantesProf.on("value", this.getPostulantProf, this.dataUserProfErr);
    },
    getPostulantProf(data) {
      this.postulantesProf = data.val();
      console.log(this.postulantesProf);
    },
    dataUserProfErr(err) {
      console.log("error");
      console.log(err);
    },
    getPostulantData() {
      for (let postulanteInfo in this.postulantesInfo) {
         let postulantes_table;
        if(this.postulantesInfo[postulanteInfo].nombre_social!= undefined){
          postulantes_table = {
          name:
            this.postulantesInfo[postulanteInfo].nombre_social +
            " " +
          this.postulantesInfo[postulanteInfo].apellido_p,
          email: this.postulantesInfo[postulanteInfo].correo,
          phone: this.postulantesInfo[postulanteInfo].telefono,
          register: this.postulantesInfo[postulanteInfo].RegistradoDate.date +" "+this.postulantesInfo[postulanteInfo].RegistradoDate.hour,
          experience: ""
        };
        }else{
          postulantes_table = {
          name:
            this.postulantesInfo[postulanteInfo].nombres+
            " " +
          this.postulantesInfo[postulanteInfo].apellido_p,
          email: this.postulantesInfo[postulanteInfo].correo,
          phone: this.postulantesInfo[postulanteInfo].telefono,
          register: this.postulantesInfo[postulanteInfo].RegistradoDate.date +" "+this.postulantesInfo[postulanteInfo].RegistradoDate.hour,
          experience: ""
        };

        }


        this.postulanteTable.push(postulantes_table)
        let postulanteData = {
          postulanteinfoPersonal: this.postulantesInfo[postulanteInfo],
          postulanteExp: this.getExperiencePostulante(postulanteInfo),
          postulanteProf: this.getFormacionPostulante(postulanteInfo)
        };
        this.postulantes.push(postulanteData);
      }
    },
    getLoginState: function(loginState) {
      this.loginState = loginState;
      this.getPostulantData();
    },
    getExperiencePostulante(id_postulante) {
      let postulanteExperiences = [];
      for (let postulanteExp in this.postulantesExp) {
        if (id_postulante == this.postulantesExp[postulanteExp].id_postulante) {
          postulanteExperiences.push(this.postulantesExp[postulanteExp]);
        }
      }
      return postulanteExperiences;
    },
    getFormacionPostulante(id_postulante) {
      let postulanteProfesion;
      for (let postulanteProf in this.postulantesProf) {
        if (
          id_postulante == this.postulantesProf[postulanteProf].id_postulante
        ) {
          postulanteProfesion = this.postulantesProf[postulanteProf];
          return postulanteProfesion;
        }
      }
    },
  }
};
</script>
