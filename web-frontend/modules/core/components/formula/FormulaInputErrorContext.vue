<template>
  <Context
    ref="context"
    class="formula-input-error-context"
    :hide-on-click-outside="false"
    data-formula-input-context
    force-position
  >
    <Alert type="error">
      <template #title>{{ formulaErrorContext.title }}</template>
      <div>
        <p :title="isHuman ? '' : formulaErrorContext.message">{{ message }}</p>
      </div>
    </Alert>
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'

export default {
  name: 'FormulaInputErrorContext',
  mixins: [context],
  props: {
    formulaErrorContext: {
      type: Object,
      required: true,
    },
  },
  computed: {
    isHuman() {
      return this.formulaErrorContext.scope === 'human'
    },
    message() {
      return this.isHuman
        ? this.formulaErrorContext.message
        : this.$t('formulaInputField.invalidSyntax')
    },
  },
  methods: {
    show(
      targetElement,
      verticalPosition = 'bottom',
      horizontalPosition = 'left',
      verticalOffset = 0,
      horizontalOffset = 0,
      width = null
    ) {
      // Ensure that the context's width is dynamically set
      // to the targetElement's width, as it can be variable.
      if (width !== null) {
        this.$refs.context.$el.style.width = `${width}px`
      }
      return this.$refs.context.show(
        targetElement,
        verticalPosition,
        horizontalPosition,
        verticalOffset,
        horizontalOffset
      )
    },
    hide() {
      this.$refs.context.hide()
      this.hideTooltip()
    },
  },
}
</script>
