<template>
  <Expandable toggle-on-click>
    <template #header="{ expanded }">
      <div class="workflow-history__divider"></div>
      <div class="workflow-history__header">
        <Icon
          v-if="props.item.status === 'success'"
          icon="iconoir-check-circle"
          type="success"
        />
        <Icon v-else icon="iconoir-warning-circle" type="error" />
        <span class="workflow-history__header-title">
          {{ historyTitlePrefix }}{{ statusTitle }}
        </span>
        <span :title="completedDate" class="workflow-history__header-date">
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
      <div
        v-for="nodeHistory in props.item.node_histories"
        :key="nodeHistory.node"
        class="workflow-history__node-histories"
      >
        <div class="workflow-history__node-history">
          <div class="workflow-history__node-history-icon">
            <i :class="getNodeIconClass(nodeHistory.node)"></i>
          </div>

          <div class="workflow-history__node-history-info">
            <div
              class="workflow-history__node-history-info-type"
              :class="{
                'workflow-history__node-history-info-type-error':
                  nodeHistory.status === 'error',
              }"
            >
              {{ nodeTypeLabel(nodeHistory.node) }}
            </div>
          </div>

          <div class="workflow-history__node-history-badge">
            <Badge
              :key="nodeHistory.node"
              rounded
              :color="nodeHistory.status === 'error' ? 'red' : 'green'"
              size="small"
            >
              {{ nodeHistoryStatus(nodeHistory.status) }}
            </Badge>
          </div>
        </div>

        <div
          v-if="nodeHistory.status === 'error'"
          class="workflow-history__node-history-error"
        >
          <div class="workflow-history__node-history-error-info">
            {{ nodeHistory.message }}
          </div>

          <Expandable toggle-on-click>
            <template #header="{ expanded }">
              <div class="workflow-history__node-history-error-expand">
                <div class="workflow-history__node-history-error-expand-label">
                  {{
                    expanded
                      ? $t('historySidePanel.errorHideDetails')
                      : $t('historySidePanel.errorShowDetails')
                  }}
                </div>

                <div class="workflow-history__node-history-error-expand-icon">
                  <Icon
                    :icon="
                      expanded
                        ? 'iconoir-nav-arrow-down'
                        : 'iconoir-nav-arrow-right'
                    "
                    type="secondary"
                  />
                </div>
              </div>
            </template>
            <template #default>
              <div class="workflow-history__node-history-error-expanded">
                {{ nodeHistory.message }}
              </div>
            </template>
          </Expandable>
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
  console.log('got node: ', getNode(nodeId))
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
