<template>
  <v-card class="mx-auto mt-5" max-width="344" >
    <v-form ref="form" v-model="valid" lazy-validation class="justify-center">
      <v-text-field v-model="name"  :rules="nameRules" label="Usuari@" required @input="message=''"></v-text-field>

      <v-text-field type="password" v-model="password" :rules="passwordRules" label="Contraseña" required @input="message=''"></v-text-field>

      <v-btn :disabled="!valid" color="success" class="mr-4" @click="validate">INGRESAR</v-btn>
      <p>{{this.message}}</p>
    </v-form>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    loginState:true,
    message:'',
    valid: true,
    name: "",
    nameRules: [
      v => !!v || "Se requiere ingresar usuari@",
    //   v => (v && v.length <= 10) || "Name must be less than 10 characters"
    ],
    password: "",
    passwordRules: [
      v => !!v || "Requiere ingresar contraseña",
    //   v => /.+@.+\..+/.test(v) || "E-mail must be valid"
    ],

  }),

  methods: {
    validate() {
     if (this.password=='1234' && this.name =='admin' && this.$refs.form.validate()) {
        this.loginState=false;
        this.$emit("validate", this.loginState);
      }else{
        this.message = 'Contraseña o nombre de usuari@ incorrecta'
      }

    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    }
  }
};
</script>