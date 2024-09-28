<script setup>
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from "@headlessui/vue";
import {defineProps, defineEmits, ref} from "vue";

// Props pour contrôler l'ouverture/fermeture de la modal
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
});

function trainYear() {
  fetch('http://localhost:5001/train-year', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  alert('Modèle de prédiction pour les années entraîné avec succès !');
}


const form = ref({
  ville: '',
})


const response = ref()
async function predictAnnee() {
  try {
    const res = await fetch('http://localhost:5001/predict-year', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form.value)
    });
    if (res.ok) {
      response.value = await res.json(); // Stocke la réponse en JSON
      console.log(response.value); // Affiche la réponse dans la console
    } else {
      alert('Modèle non entraîné pour les années !')
    }
  } catch (error) {
    console.error('Error:', error);
  }
}


// Événements émis pour informer le parent de la fermeture de la modal
const emit = defineEmits(['close']);

// Fonction pour fermer la modal
function closeModal() {
  emit('close');
}
</script>

<template>
  <!-- TransitionRoot pour la modal -->
  <TransitionRoot :show="isOpen" appear as="template">
    <Dialog as="div" class="relative z-10" @close="closeModal">
      <div class="fixed inset-0 bg-black/30" />

      <!-- Modal Content -->
      <div class="fixed inset-0 flex items-center justify-center p-4 text-center">
        <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
        >
          <DialogPanel class="w-full max-w-md transform bg-white p-6 rounded-lg shadow-xl">
            <!-- Titre de la modal -->
            <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
              Modèle de Prédiction Année
            </DialogTitle>

            <!-- Bouton pour fermer la modal -->
            <button @click="closeModal" class="absolute top-2 right-2 text-gray-400 hover:text-gray-600 focus:outline-none">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            <!-- Contenu de la modal -->
            <div class="mt-4">
              <p class="text-sm text-gray-500">
                Ici, vous pouvez entraîner et utiliser votre modèle de prédiction.
              </p>

              <a @click="trainYear()" class="group flex mt-5 items-center px-3 py-2 cursor-pointer text-sm font-medium text-white transition-all duration-200 bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 shadow-md hover:shadow-lg">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 mr-2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5m-9-6h.008v.008H12v-.008ZM12 15h.008v.008H12V15Zm0 2.25h.008v.008H12v-.008ZM9.75 15h.008v.008H9.75V15Zm0 2.25h.008v.008H9.75v-.008ZM7.5 15h.008v.008H7.5V15Zm0 2.25h.008v.008H7.5v-.008Zm6.75-4.5h.008v.008h-.008v-.008Zm0 2.25h.008v.008H16.5V15Z" />
                </svg>
                <span class="mr-2">Entrainer le modèle de prédiction pour les années</span>
              </a>

              <!-- Formulaire pour envoyer des données au backend -->
              <form @submit.prevent="predictAnnee">
                <div class="mt-4">
                  <label class="block text-sm font-medium text-gray-700">Ville</label>
                  <select v-model="form.ville" required class="block w-full mt-1 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    <option value="lyon">Lyon</option>
                    <option value="paris">Paris</option>
                    <option value="marseille">Marseille</option>
                  </select>
                </div>

                <div class="mt-4">
                  <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                    Prédiction
                  </button>
                </div>
              </form>

              <div v-if="response">
                <p class="mt-4 text-sm text-gray-500">
                  Prédiction Année: {{ response ? parseInt(response.predicted_year)  : 'Aucune prédiction' }}
                </p>
              </div>
            </div>
          </DialogPanel>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<style scoped>
/* Styles optionnels supplémentaires */
</style>
