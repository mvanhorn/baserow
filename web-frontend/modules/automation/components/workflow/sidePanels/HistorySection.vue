<template>
  <Expandable toggle-on-click>
    <template #header="{ expanded }">
      <div class="history-section__divider"></div>
      <div class="history-section__header">
        <Icon
          v-if="props.item.status === 'success'"
          icon="iconoir-check-circle"
          type="success"
        />
        <Icon v-else icon="iconoir-warning-circle" type="error" />
        <span class="history-section__header-title">
          {{ historyTitlePrefix }}{{ statusTitle }}
        </span>
        <span :title="completedDate" class="history-section__header-date">
          {{ humanCompletedDate }}
        </span>
        <Icon
          :icon="
            expanded ? 'iconoir-nav-arrow-down' : 'iconoir-nav-arrow-right'
          "
          type="secondary"
        />
      </div>
    </template>

    <template #default>
      <!-- <div class="history-section__message">
        {{ historyMessage }}
      </div> -->
      <div
        v-for="nodeHistory in props.item.node_histories"
        :key="nodeHistory.id"
        class="history-section__node-histories"
      >
        <div class="history-section__node-history">
          <div class="history-section__node-history-info">
            <div class="history-section__node-history-icon">
              <i :class="getNodeIconClass(nodeHistory.id)"></i>
            </div>
            <div
              class="history-section__node-history-type"
              :class="{
                'history-section__node-history-type-error':
                  nodeHistory.status === 'error',
              }"
            >
              {{ nodeTypeLabel(nodeHistory.id) }}
            </div>
          </div>
          <div class="history-section__node-history-status">
            <Badge
              :key="nodeHistory.id"
              rounded
              :color="nodeHistory.status === 'error' ? 'red' : 'green'"
              size="small"
            >
              {{ nodeHistoryStatus(nodeHistory.status) }}
            </Badge>
          </div>
        </div>
      </div>
    </template>
  </Expandable>
</template>

<script setup>
import moment from '@baserow/modules/core/moment'
import { getUserTimeZone } from '@baserow/modules/core/utils/date'
import { useStore } from 'vuex'

const app = useNuxtApp()

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
})

const store = useStore()
const workflow = inject('workflow')
const automation = inject('automation')

const statusTitle = computed(() => {
  switch (props.item.status) {
    case 'success':
      return app.$i18n.t('historySidePanel.statusSuccess')
    case 'error':
      return app.$i18n.t('historySidePanel.statusError')
    default:
      return app.$i18n.t('historySidePanel.statusDisabled')
  }
})

const getNode = (nodeId) => {
  return store.getters['automationWorkflowNode/findById'](
    workflow.value,
    nodeId
  )
}
const getNodeType = (nodeId) => {
  console.log('getting nodeId: ', nodeId)
  return app.$registry.get('node', getNode(nodeId).type)
}

const getNodeIconClass = (nodeId) => {
  const nodeType = getNodeType(nodeId)
  console.log('nodeType: ', nodeType)
  return nodeType.iconClass
}

const nodeTypeLabel = (nodeId) => {
  const nodeType = getNodeType(nodeId)
  const node = getNode(nodeId)
  return nodeType.getLabel({
    automation: automation.value,
    node: node,
  })
}

const completedDate = computed(() => {
  return moment
    .utc(props.item.completed_on)
    .tz(getUserTimeZone())
    .format('YYYY-MM-DD HH:mm:ss')
})

const nodeHistoryStatus = (status) => {
  switch (status) {
    case 'success':
      return app.$i18n.t('historySidePanel.statusSuccessBadge')
    case 'error':
      return app.$i18n.t('historySidePanel.statusErrorBadge')
    default:
      return app.$i18n.t('historySidePanel.statusErrorBadge')
  }
}

const humanCompletedDate = computed(() => {
  return moment.utc(props.item.completed_on).tz(getUserTimeZone()).fromNow()
})

const historyTitlePrefix = computed(() => {
  return props.item.is_test_run === true
    ? `[${app.$i18n.t('historySidePanel.testRun')}] `
    : ''
})

const historyMessage = computed(() => {
  if (props.item.status === 'success') {
    const start = new Date(props.item.started_on)
    const end = new Date(props.item.completed_on)

    const deltaMs = end - start
    if (deltaMs < 1000) {
      return app.$i18n.t('historySidePanel.completedInLessThanSecond')
    } else {
      const deltaSeconds = deltaMs / 1000
      return app.$i18n.t('historySidePanel.completedInSeconds', {
        s: deltaSeconds.toFixed(2),
      })
    }
  } else {
    return props.item.message
  }
})
</script>
