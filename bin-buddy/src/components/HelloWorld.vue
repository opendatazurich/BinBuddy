<template>
  <v-container>
    <!-- Gemeinde Auswahl -->
    <v-row class="text-center">
      <v-col cols="12">
        <v-autocomplete
          deletable-chips
          filled
          :items="municipalities"
          label="Gemeinde"
        ></v-autocomplete>
      </v-col>
    </v-row>
    <!-- Gemeinde Auswahl END -->
    <v-row>
      <v-btn color="primary" elevation="2" outlined @click="addRow"
        >Neuer Eintrag</v-btn
      >
    </v-row>

    <!-- FORMULAR -->
    <v-row>
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-row v-for="row in formData" :key="row.id">
          <!-- Garbage Type -->
          <v-select
            v-model="row.select"
            :items="garbageType"
            :rules="[(v) => !!v || 'Bitte einen Typ auswählen.']"
            label="Typ"
            required
          ></v-select>
          <!-- Garbage Type END -->

          <v-checkbox
            v-model="row.checkbox"
            label="Entsorgungsserie?"
          ></v-checkbox>
          <!-- Date-Series -->
          <v-row v-if="row.checkbox">
            <v-col>
              <v-select
                v-model="row.value"
                :items="days"
                attach
                chips
                label="Wann?"
                multiple
              ></v-select>
              <v-text-field
                v-model="row.repetition"
                label="Wiederholung jede(n):"
                type="number"
                :rules="[numberRule]"
              ></v-text-field>
              <v-radio-group v-model="row.radioGroup">
                <v-radio label="Tag(e)" value="radio-1"></v-radio>
                <v-radio label="Woche(n)" value="radio-2"></v-radio>
                <v-radio label="Monat(e)" value="radio-3"></v-radio>
                <v-radio label="Jahr(e)" value="radio-4"></v-radio>
              </v-radio-group>
            </v-col>
          </v-row>
          <!-- Date-Series END -->
          <!-- Single Datetime -->
          <v-row v-if="!row.checkbox">
            <v-date-picker
              v-model="picker"
              label="Wähle das Datum"
            ></v-date-picker>
            <v-time-picker label="Wähle die Zeit" format="24hr"></v-time-picker>
          </v-row>
        </v-row>
        <!-- Single Datetime END -->

        <!-- Preview -->
        <v-textarea
          readonly
          filled
          label="Vorschau"
          auto-grow
          :value="JSON.stringify(formData)"
        >
          {{ formData }}</v-textarea
        >
        <!-- Preview END -->
        <v-btn
          :disabled="!valid"
          color="success"
          class="mr-4"
          @click="validate"
        >
          Download
        </v-btn>
        <v-btn color="error" class="mr-4" @click="reset"> Reset </v-btn>
      </v-form>
    </v-row>
    <!-- FORMULAR END -->
  </v-container>
</template>

<script>
export default {
  name: "HelloWorld",

  data: () => ({
    formData: [],
    municipalities: [
      "Bülach",
      "Lausanne",
      "Chur",
      "Bitsch",
      "Sarnen",
      "Zollikofen",
    ],
    valid: true,
    garbageType: ["Abfall", "Papier", "Sperrgut", "Holz"],
    picker: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .substr(0, 10),
    days: [
      "Montag",
      "Dienstag",
      "Mittwoch",
      "Donnerstag",
      "Freitag",
      "Samstag",
      "Sonntag",
    ],
    numberRule: (v) => {
      if (!v.trim()) return true;
      if (!isNaN(parseFloat(v)) && v > 0) return true;
      return "Anzahl muss eine positive Nummer sein";
    },
  }),
  methods: {
    addRow() {
      this.formData.push({
        id: new Date().valueOf(),
        select: true,
        checkbox: true,
        value: null,
        repetition: "0",
        radioGroup: null,
        menu2: false,
      });
      console.log("Added item: " + this.formData.at(-1).id);
    },
    /* TODO: DOWNLOAD AS CSV */
    validate() {
      this.$refs.form.validate();
    },
    reset() {
      while (this.formData.length > 0) {
        this.formData.pop();
      }
      this.$refs.form.reset();
    },
  },
};
</script>
