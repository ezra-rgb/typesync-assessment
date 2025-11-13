<template>
  <div class="radar-chart">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

export default {
  name: 'RadarChart',
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chart: null
    }
  },
  mounted() {
    this.createChart()
  },
  watch: {
    data: {
      handler() {
        if (this.chart) {
          this.chart.destroy()
        }
        this.createChart()
      },
      deep: true
    }
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy()
    }
  },
  methods: {
    createChart() {
      const ctx = this.$refs.chartCanvas.getContext('2d')
      
      this.chart = new ChartJS(ctx, {
        type: 'radar',
        data: this.data,
        options: {
          responsive: true,
          maintainAspectRatio: true,
          scales: {
            r: {
              beginAtZero: true,
              max: 100,
              ticks: {
                stepSize: 20
              },
              grid: {
                color: '#e0e0e0'
              },
              angleLines: {
                color: '#e0e0e0'
              }
            }
          },
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                padding: 20,
                font: {
                  size: 14
                }
              }
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return context.dataset.label + ': ' + context.parsed.r + '%'
                }
              }
            }
          },
          elements: {
            line: {
              borderWidth: 3
            },
            point: {
              radius: 5,
              hoverRadius: 7
            }
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.radar-chart {
  max-width: 500px;
  margin: 0 auto;
  padding: 1rem;
}

canvas {
  max-width: 100%;
  height: auto;
}
</style>